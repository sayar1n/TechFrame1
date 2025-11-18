'use client';

import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import DefectForm from '@/app/components/DefectForm';
import { fetchDefectById, updateDefect, fetchProjects, fetchUsers } from '@/app/utils/api';
import { useAuth } from '@/app/context/AuthContext';
import { Defect, DefectCreate, Project, User } from '@/app/types';
import styles from './EditDefectPage.module.scss'; // Предполагается, что файл стилей будет создан

interface EditDefectPageProps {
  params: {
    id: string;
  };
}

const EditDefectPage = ({ params }: EditDefectPageProps) => {
  const [defectId, setDefectId] = useState<number | null>(null);
  const { token, isLoading: authLoading } = useAuth();
  const router = useRouter();
  const [defect, setDefect] = useState<Defect | null>(null);
  const [projects, setProjects] = useState<Project[]>([]);
  const [users, setUsers] = useState<User[]>([]);
  const [loadingData, setLoadingData] = useState(false); // Изменяем имя стейта
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // Извлекаем id из pathname после гидратации на клиенте
    if (typeof window !== 'undefined') {
      const pathParts = window.location.pathname.split('/');
      const idFromPath = parseInt(pathParts[pathParts.length - 2], 10); // /defects/[id]/edit
      if (!isNaN(idFromPath)) {
        setDefectId(idFromPath);
      }
    }
  }, []);

  useEffect(() => {
    const fetchData = async () => {
      if (!token || authLoading || defectId === null || isNaN(defectId)) return;

      setLoadingData(true); // Устанавливаем загрузку данных
      try {
        const fetchedDefect = await fetchDefectById(token, defectId);
        setDefect(fetchedDefect);
        const fetchedProjects = await fetchProjects(token);
        setProjects(fetchedProjects);
        const fetchedUsers = await fetchUsers(token);
        setUsers(fetchedUsers);
      } catch (err: any) {
        setError(err.message || 'Не удалось загрузить данные дефекта.');
      } finally {
        setLoadingData(false); // Снимаем загрузку данных
      }
    };

    fetchData();
  }, [token, authLoading, defectId]);

  const handleSubmit = async (defectData: DefectCreate) => {
    if (!token || defectId === null || isNaN(defectId)) {
      setError('Для обновления дефекта необходимо войти в систему или указать корректный ID.');
      return;
    }

    setLoadingData(true); // Устанавливаем загрузку данных
    setError(null);
    try {
      await updateDefect(token, defectId, defectData);
      router.push(`/defects/${defectId}`);
    } catch (err: any) {
      setError(err.message || 'Не удалось обновить дефект.');
    } finally {
      setLoadingData(false); // Снимаем загрузку данных
    }
  };

  if (authLoading || loadingData || defectId === null || isNaN(defectId)) { // Используем loadingData
    return <div>Загрузка...</div>;
  }

  if (error) {
    return <div className={styles.error}>{error}</div>;
  }

  if (!defect) {
    return <div>Дефект не найден.</div>;
  }

  return (
    <div className={styles.editDefectContainer}>
      <h1>Редактировать дефект: {defect.title}</h1>
      <DefectForm
        initialData={defect}
        onSubmit={handleSubmit}
        isLoading={loadingData} // Передаем loadingData в DefectForm
        error={error}
        projects={projects}
        users={users}
      />
    </div>
  );
};

export default EditDefectPage;
