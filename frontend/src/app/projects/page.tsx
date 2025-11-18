'use client';

import React, { useEffect, useState, useMemo } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { Project } from '@/app/types';
import { fetchProjects } from '@/app/utils/api';
import { useAuth } from '@/app/context/AuthContext';
import styles from './ProjectsPage.module.scss';

const ProjectsPage = () => {
  const { token, isLoading, user } = useAuth();
  const [projects, setProjects] = useState<Project[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [sortBy, setSortBy] = useState<keyof Project>('created_at');
  const [sortOrder, setSortOrder] = useState<'asc' | 'desc'>('desc');
  const router = useRouter();

  useEffect(() => {
    const getProjects = async () => {
      if (!token || isLoading) return;

      try {
        const fetchedProjects = await fetchProjects(token);
        setProjects(fetchedProjects);
      } catch (err: any) {
        setError(err.message || 'Не удалось загрузить проекты.');
      }
    };

    getProjects();
  }, [token, isLoading]);

  const handleCreateProjectClick = () => {
    router.push('/projects/new');
  };

  const filteredAndSortedProjects = useMemo(() => {
    let filtered = projects.filter(project =>
      project.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
      (project.description && project.description.toLowerCase().includes(searchTerm.toLowerCase()))
    );

    filtered.sort((a, b) => {
      const aValue = a[sortBy];
      const bValue = b[sortBy];

      if (typeof aValue === 'string' && typeof bValue === 'string') {
        return sortOrder === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
      } else if (typeof aValue === 'number' && typeof bValue === 'number') {
        return sortOrder === 'asc' ? aValue - bValue : bValue - aValue;
      }
      return 0;
    });

    return filtered;
  }, [projects, searchTerm, sortBy, sortOrder]);

  if (isLoading) {
    return <div>Загрузка проектов...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  const canCreateProject = user && (user.role === 'manager' || user.role === 'engineer');

  return (
    <div className={styles.projectsContainer}>
      <div className={styles.headerActions}>
        <h1>Страница проектов</h1>
        {canCreateProject && (
          <button onClick={handleCreateProjectClick} className={styles.createButton}>
            Создать новый проект
          </button>
        )}
      </div>

      <div className={styles.filters}>
        <input
          type="text"
          placeholder="Поиск по названию или описанию..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className={styles.searchInput}
        />
        <select value={sortBy} onChange={(e) => setSortBy(e.target.value as keyof Project)} className={styles.sortSelect}>
          <option value="created_at">Дата создания</option>
          <option value="title">Название</option>
        </select>
        <select value={sortOrder} onChange={(e) => setSortOrder(e.target.value as 'asc' | 'desc')} className={styles.sortSelect}>
          <option value="asc">По возрастанию</option>
          <option value="desc">По убыванию</option>
        </select>
      </div>

      {filteredAndSortedProjects.length === 0 ? (
        <p>Проектов пока нет.</p>
      ) : (
        <table className={styles.projectsTable}>
          <thead>
            <tr>
              <th>ID</th>
              <th>Название</th>
              <th>Описание</th>
              <th>Владелец</th>
              <th>Дата создания</th>
            </tr>
          </thead>
          <tbody>
            {filteredAndSortedProjects.map((project) => (
              <tr key={project.id} className={styles.projectRow}>
                <td>
                  <Link href={`/projects/${project.id}`}>{project.id}</Link>
                </td>
                <td>
                  <Link href={`/projects/${project.id}`}>{project.title}</Link>
                </td>
                <td>{project.description || 'Нет описания'}</td>
                <td>{project.owner_id}</td>
                <td>{new Date(project.created_at).toLocaleDateString()}</td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default ProjectsPage;
