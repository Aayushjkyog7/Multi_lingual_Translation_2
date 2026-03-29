import React from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import './SwamijiPage.css';

function SwamijiPage() {
  const { t } = useTranslation();

  return (
    <div className="swamiji-app">
      <div className="swamiji-container">
        <header className="swamiji-header">
          <Link to="/" className="swamiji-back">
            {t('swamiji.backHome')}
          </Link>
          <div className="swamiji-hero">
            <p className="swamiji-eyebrow">{t('swamiji.eyebrow')}</p>
            <h1 className="swamiji-title">{t('swamiji.title')}</h1>
            <p className="swamiji-subtitle">
              {t('swamiji.subtitle')}
            </p>
          </div>
        </header>

        <main className="swamiji-main">
          <article className="swamiji-section swamiji-section--accent">
            <div className="swamiji-section-head">
              <span className="swamiji-badge">{t('swamiji.part1')}</span>
              <h2 className="swamiji-section-title">{t('swamiji.earlyLifeTitle')}</h2>
              <h3 className="swamiji-section-subtitle">{t('swamiji.formativeYears')}</h3>
            </div>
            <div className="swamiji-body">
              <p>{t('swamiji.earlyP1')}</p>
              <p>{t('swamiji.earlyP2')}</p>
              <p>{t('swamiji.earlyP3')}</p>
            </div>
          </article>

          <article className="swamiji-section">
            <div className="swamiji-section-head">
              <span className="swamiji-badge swamiji-badge--secondary">{t('swamiji.part2')}</span>
              <h2 className="swamiji-section-title">{t('swamiji.journeyTitle')}</h2>
              <h3 className="swamiji-section-subtitle">{t('swamiji.spiritualCalling')}</h3>
            </div>
            <div className="swamiji-body">
              <p>{t('swamiji.journeyP1')}</p>
              <p>{t('swamiji.journeyP2')}</p>
            </div>
          </article>
        </main>
      </div>
    </div>
  );
}

export default SwamijiPage;
