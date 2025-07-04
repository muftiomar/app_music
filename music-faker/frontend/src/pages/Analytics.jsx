import React, { useEffect, useState } from 'react';
import ChartBlock from '../components/ChartBlock';

const Analytics = () => {
  const [metrics, setMetrics] = useState(null);
  const [source, setSource] = useState('fake'); // fake or real
  const [currentIndex, setCurrentIndex] = useState(0);

  const fetchMetrics = async () => {
    const url = source === 'fake'
      ? '/data/fake-metrics.json'
      : '/data/real-metrics.json';

    try {
      const res = await fetch(url);
      const data = await res.json();
      setMetrics(data);
    } catch (err) {
      console.error('Erreur de chargement des métriques:', err);
    }
  };

  useEffect(() => {
    fetchMetrics(); // initial load
    const interval = setInterval(() => {
      fetchMetrics();
    }, 10000); // auto-refresh every 10s
    return () => clearInterval(interval);
  }, [source]);

  if (!metrics) return <p>Chargement des métriques...</p>;

  // Liste ordonnée des métriques à afficher
  const metricList = [
    {
      title: 'Écoutes par genre',
      type: 'bar',
      labels: Object.keys(metrics.genres),
      data: Object.values(metrics.genres),
    },
    {
      title: 'Top artistes',
      type: 'pie',
      labels: Object.keys(metrics.top_artists),
      data: Object.values(metrics.top_artists),
    },
    metrics.hours && {
      title: 'Écoutes par heure',
      type: 'line',
      labels: Object.keys(metrics.hours),
      data: Object.values(metrics.hours),
    }
  ].filter(Boolean); // ignore undefined

  const current = metricList[currentIndex];

  const goPrev = () => {
    setCurrentIndex((prev) => (prev === 0 ? metricList.length - 1 : prev - 1));
  };

  const goNext = () => {
    setCurrentIndex((prev) => (prev === metricList.length - 1 ? 0 : prev + 1));
  };

  return (
    <div style={{ position: 'relative' }}>
      <h1 style={{ textAlign: 'center' }}>📊 Statistiques musicales</h1>

      <div style={{ marginBottom: '1rem', textAlign: 'center' }}>
        <label>Source de données : </label>
        <select
          value={source}
          onChange={(e) => setSource(e.target.value)}
          style={{ padding: '0.5rem', fontSize: '1rem' }}
        >
          <option value="fake">Fake (simulée)</option>
          <option value="real">Réelle (dataset)</option>
        </select>
        <p style={{ fontSize: '0.8rem', color: '#9ca3af' }}>
          (Données mises à jour toutes les 10 secondes)
        </p>
      </div>

      <div style={{ position: 'relative', padding: '2rem 0' }}>
        {/* Flèche gauche */}
        <button
          onClick={goPrev}
          style={{
            position: 'absolute',
            left: '-2rem',
            top: '50%',
            transform: 'translateY(-50%)',
            fontSize: '2rem',
            background: 'transparent',
            border: 'none',
            color: 'var(--text)',
            cursor: 'pointer'
          }}
        >
          ⬅
        </button>

        {/* Le graphique */}
        <ChartBlock
          title={current.title}
          type={current.type}
          data={{
            labels: current.labels,
            datasets: [{
              label: current.title,
              data: current.data,
              backgroundColor: ['#10b981', '#3b82f6', '#facc15', '#f472b6', '#a78bfa', '#f87171']
            }]
          }}
        />

        {/* Flèche droite */}
        <button
          onClick={goNext}
          style={{
            position: 'absolute',
            right: '-2rem',
            top: '50%',
            transform: 'translateY(-50%)',
            fontSize: '2rem',
            background: 'transparent',
            border: 'none',
            color: 'var(--text)',
            cursor: 'pointer'
          }}
        >
          ➡
        </button>
      </div>
    </div>
  );
};

export default Analytics;
