import React from 'react';
import { Bar, Pie } from 'react-chartjs-2';
import {
  Chart as ChartJS,
  BarElement,
  CategoryScale,
  LinearScale,
  Tooltip,
  Legend,
  ArcElement
} from 'chart.js';

ChartJS.register(BarElement, CategoryScale, LinearScale, ArcElement, Tooltip, Legend);

const ChartBlock = ({ title, data, type }) => {
  return (
    <div style={{ padding: '1rem', border: '1px solid #ddd', borderRadius: '8px', background: '#f9f9f9' }}>
      <h3 style={{ marginBottom: '1rem' }}>{title}</h3>
      {type === 'bar' && <Bar data={data} />}
      {type === 'pie' && <Pie data={data} />}
    </div>
  );
};

export default ChartBlock;
