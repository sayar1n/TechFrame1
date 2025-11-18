'use client';

import React from 'react';
import AuthGuard from '@/app/components/AuthGuard';
import styles from './ReportsPage.module.scss';

const ReportsPage = () => {
  const handleExport = (format: 'csv' | 'excel') => {
    alert(`Экспорт отчета в формат: ${format.toUpperCase()}`);
    // Здесь будет реализована логика для вызова API экспорта
  };

  return (
    <AuthGuard roles={['manager', 'observer']}>
      <div className={styles.reportsContainer}>
        <h1>Страница отчетов</h1>

        <section className={styles.reportSection}>
          <h2>Экспорт отчетов</h2>
          <div className={styles.exportActions}>
            <button onClick={() => handleExport('csv')} className={styles.exportButton}>
              Экспорт в CSV
            </button>
            <button onClick={() => handleExport('excel')} className={styles.exportButton}>
              Экспорт в Excel
            </button>
          </div>
        </section>

        <section className={styles.reportSection}>
          <h2>Аналитические отчеты</h2>
          <p>Здесь будут представлены аналитические графики и статистика по дефектам и проектам.</p>
          <div className={styles.analyticsPlaceholder}>
            {/* Здесь можно будет интегрировать компоненты для построения графиков */}
            <p>Место для графиков и диаграмм.</p>
            <p>Например: количество дефектов по статусам, по приоритетам, по исполнителям, динамика создания/закрытия дефектов.</p>
          </div>
        </section>
      </div>
    </AuthGuard>
  );
};

export default ReportsPage;
