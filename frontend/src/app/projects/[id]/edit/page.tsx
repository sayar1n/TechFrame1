'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import ProjectForm from '../../../components/ProjectForm';
import { fetchProjectById, updateProject } from '../../../utils/api';
import { useAuth } from '../../../context/AuthContext';
import { Project, ProjectCreate } from '../../../types';
import styles from './EditProjectPage.module.scss'; // Предполагается, что файл стилей будет создан

interface EditProjectPageProps {
  params: {
    id: string;
  };
}

const EditProjectPage = ({ params }: EditProjectPageProps) => {
  const { id } = params;
  const projectId = parseInt(id, 10);
  const { token, isLoading: authLoading } = useAuth();
  const router = useRouter();
  const [project, setProject] = useState<Project | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const getProject = async () => {
      if (!token || authLoading || isNaN(projectId)) return;

      try {
        const fetchedProject = await fetchProjectById(token, projectId);
        setProject(fetchedProject);
      } catch (err: any) {
        setError(err.message || 'Не удалось загрузить данные проекта.');
      }
    };

    getProject();
  }, [token, authLoading, projectId]);

  const handleSubmit = async (projectData: ProjectCreate) => {
    if (!token || isNaN(projectId)) {
      setError('Для обновления проекта необходимо войти в систему или указать корректный ID.');
      return;
    }

    setIsLoading(true);
    setError(null);
    try {
      await updateProject(token, projectId, projectData);
      router.push(`/projects/${projectId}`);
    } catch (err: any) {
      setError(err.message || 'Не удалось обновить проект.');
    } finally {
      setIsLoading(false);
    }
  };

  if (authLoading || isNaN(projectId)) {
    return <div>Загрузка...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  if (!project) {
    return <div>Проект не найден.</div>;
  }

  return (
    <div className={styles.editProjectContainer}>
      <h1>Редактировать проект: {project.title}</h1>
      <ProjectForm
        initialData={project}
        onSubmit={handleSubmit}
        isLoading={isLoading}
        error={error}
      />
    </div>
  );
};

export default EditProjectPage;
