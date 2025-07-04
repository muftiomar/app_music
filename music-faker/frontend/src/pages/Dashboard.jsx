import React from 'react';
import MusicCard from '../components/MusicCard';

const mockSongs = [
    {
      title: 'Désolé',
      artist: 'Sexion d’Assaut',
      image: 'https://i.discogs.com/M6VIoyxIGfMWkhPH0o9EhM6pgtqB51sltdG5C5m886k/rs:fit/g:sm/q:90/h:600/w:597/czM6Ly9kaXNjb2dz/LWRhdGFiYXNlLWlt/YWdlcy9SLTMzMTQ3/MDA2LTE3Mzk2MzEw/OTgtMjQwOS5qcGVn.jpeg',
      duration: '3:25'
    },
    {
      title: 'Industry Baby',
      artist: 'Lil Nas X',
      image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5e43SKeVrL7zsoWdjR1K9FwGfFwH9ZS1nXg&s',
      duration: '2:45'
    },
    {
      title: 'Djadja',
      artist: 'Aya Nakamura',
      image: 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTj542kRAOUNNa57IhDJI-wEoglviZ9yoLu1Q&s',
      duration: '3:30'
    }
  ];
  

const Dashboard = () => {
  return (
    <div>
      <h1>🎧 Explore les sons</h1>
      <div style={{
        display: 'flex',
        gap: '1.5rem',
        marginTop: '2rem',
        flexWrap: 'wrap'
      }}>
        {mockSongs.map((song, idx) => (
          <MusicCard
            key={idx}
            title={song.title}
            artist={song.artist}
            image={song.image}
            duration={song.duration}
          />
        ))}
      </div>
    </div>
  );
};

export default Dashboard;
