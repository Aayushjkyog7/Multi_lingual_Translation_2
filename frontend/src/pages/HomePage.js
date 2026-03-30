import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import axios from 'axios';
import '../App.css';

const API_BASE_URL = 'http://localhost:8000/api';

function HomePage() {
  const { t, i18n } = useTranslation();
  const [contentTypes, setContentTypes] = useState([]);
  const [contentTypesLoading, setContentTypesLoading] = useState(true);
  const [contentTypesError, setContentTypesError] = useState(null);
  const [selectedType, setSelectedType] = useState(null);
  const [contentData, setContentData] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    setContentTypesError(null);
    axios.get(`${API_BASE_URL}/content-types`)
      .then(response => {
        setContentTypes(response.data.contentTypes);
        setContentTypesLoading(false);
      })
      .catch(err => {
        setContentTypesError(t('failedToLoadContentTypes'));
        setContentTypesLoading(false);
        console.error(err);
      });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const handleTypeSelect = (type) => {
    setSelectedType(type);
    setLoading(true);
    setError(null);
    setContentData([]);

    const currentLang = i18n.language || 'en';
    const translatedContentTypes = ['videos', 'moments'];
    const url = translatedContentTypes.includes(type)
      ? `${API_BASE_URL}/content/${type}?lang=${currentLang}`
      : `${API_BASE_URL}/content/${type}`;

    axios.get(url)
      .then(response => {
        setContentData(response.data.data);
        setLoading(false);
      })
      .catch(err => {
        setError(`${t('failedToLoad')} ${type}`);
        setLoading(false);
        console.error(err);
      });
  };

  const handleLanguageToggle = () => {
    const newLanguage = i18n.language === 'en' ? 'hi' : 'en';
    i18n.changeLanguage(newLanguage);

    if (selectedType === 'videos' || selectedType === 'moments') {
      setLoading(true);
      axios.get(`${API_BASE_URL}/content/${selectedType}?lang=${newLanguage}`)
        .then(response => {
          setContentData(response.data.data);
          setLoading(false);
        })
        .catch(err => {
          setError(`${t('failedToLoad')} ${selectedType}`);
          setLoading(false);
          console.error(err);
        });
    }
  };

  const getTypeLabel = (type) => {
    return t(`contentTypes.${type}`, type.charAt(0).toUpperCase() + type.slice(1));
  };

  const getIdField = (type) => {
    const idFields = {
      videos: 'video_id',
      moments: 'moment_id',
      podcasts: 'podcast_id',
      articles: 'article_id'
    };
    return idFields[type] || 'id';
  };

  return (
    <div className="app">
      <div className="container">
        <div className="header-section">
          <h1 className="title">{t('appTitle')}</h1>
          <div className="header-actions">
            <Link to="/swamiji" className="nav-link">
              Swamiji
            </Link>
            <button
              className="language-toggle"
              onClick={handleLanguageToggle}
              title={i18n.language === 'en' ? t('switchToHindi') : t('switchToEnglish')}
            >
              {i18n.language === 'en' ? '🇮🇳 हिंदी' : '🇬🇧 English'}
            </button>
          </div>
        </div>

        <div className="content-types-list">
          <h2 className="section-title">{t('selectContentType')}</h2>
          {contentTypesLoading && (
            <div className="loading">{t('loading')}</div>
          )}
          {contentTypesError && (
            <div className="error">{contentTypesError}</div>
          )}
          {!contentTypesLoading && !contentTypesError && (
            <div className="type-buttons">
              {contentTypes.map(type => (
                <button
                  key={type}
                  className={`type-button ${selectedType === type ? 'active' : ''}`}
                  onClick={() => handleTypeSelect(type)}
                >
                  {getTypeLabel(type)}
                </button>
              ))}
            </div>
          )}
        </div>

        {selectedType && (
          <div className="content-display">
            <div className="section-header">
              <h2 className="section-title">
                {getTypeLabel(selectedType)} ({contentData.length} {t('items')})
              </h2>
            </div>

            {loading && (
              <div className="loading">{t('loading')}</div>
            )}

            {error && (
              <div className="error">{error}</div>
            )}

            {!loading && !error && contentData.length === 0 && (
              <div className="no-data">{t('noData')}</div>
            )}

            {!loading && !error && contentData.length > 0 && (
              <div className="content-grid">
                {contentData.map((item) => (
                  <div key={item.id} className="content-card">
                    <div className="content-id">
                      {getIdField(selectedType).replace('_id', '').toUpperCase()}: {item[getIdField(selectedType)]}
                    </div>
                    <h3 className="content-title">{item.title}</h3>
                    <p className="content-description">{item.description}</p>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default HomePage;
