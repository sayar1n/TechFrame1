'use client';

import React, { useState } from 'react';
import { useAuth } from '@/app/context/AuthContext';
import AuthGuard from '@/app/components/AuthGuard';
import { exportDefectsToCsvExcel } from '@/app/utils/api';
import styles from './ReportsPage.module.scss';

const ReportsPage = () => {
  const { token, user } = useAuth();
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleExport = async (format: "csv" | "xlsx") => {
    if (!token) {
      setError('Для экспорта отчетов необходимо войти в систему.');
      return;
    }
    setIsLoading(true);
    setError(null);
    try {
      const blob = await exportDefectsToCsvExcel(token, format);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `defects_report.${format}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      alert(`Отчет успешно экспортирован в формат ${format.toUpperCase()}.`);
    } catch (err: any) {
      setError(err.message || `Не удалось экспортировать отчет в формат ${format.toUpperCase()}.`);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <AuthGuard roles={['manager', 'observer', 'admin']}>
      <div className={styles.reportsContainer}>
        <h1>Аналитические отчеты</h1>
        {error && <p className={styles.error}>{error}</p>}
        {isLoading && <p>Генерация отчета...</p>}

        <div className={styles.exportSection}>
          <h2>Экспорт отчетов</h2>
          <button onClick={() => handleExport('csv')} disabled={isLoading} className={styles.exportButton}>
            Экспорт в CSV
          </button>
          <button onClick={() => handleExport('xlsx')} disabled={isLoading} className={styles.exportButton}>
            Экспорт в Excel
          </button>
        </div>

        <div className={styles.chartsSection}>
          <h2>Графики и статистика</h2>
          <div className={styles.chartPlaceholder}>
            <p>Место для графиков: Количество дефектов по статусам</p>
          </div>
          <div className={styles.chartPlaceholder}>
            <p>Место для графиков: Количество дефектов по приоритетам</p>
          </div>
          <div className={styles.chartPlaceholder}>
            <p>Место для графиков: Динамика создания/закрытия дефектов</p>
          </div>
        </div>
      </div>
    </AuthGuard>
  );
};

export default ReportsPage;
