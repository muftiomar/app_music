import React, { useState, useRef } from 'react';

const MusicCard = ({ title, artist, image, duration, audio }) => {
  const [hovered, setHovered] = useState(false);
  const audioRef = useRef(null);

  const togglePlay = () => {
    if (!audioRef.current) return;
    if (audioRef.current.paused) {
      audioRef.current.play();
    } else {
      audioRef.current.pause();
    }
  };

  return (
    <div
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        background: 'var(--card-bg)',
        borderRadius: '10px',
        padding: '1rem',
        width: '200px',
        transition: 'transform 0.3s, box-shadow 0.3s',
        transform: hovered ? 'scale(1.05)' : 'scale(1)',
        boxShadow: hovered ? '0 0 20px rgba(34,197,94,0.4)' : 'none',
        cursor: 'pointer',
        position: 'relative'
      }}
    >
      <img
        src={image}
        alt={title}
        style={{ width: '100%', borderRadius: '8px', marginBottom: '0.5rem' }}
      />
      <h3 style={{ margin: '0.5rem 0', fontSize: '1rem' }}>{title}</h3>
      <p style={{ color: '#9ca3af', margin: '0' }}>{artist}</p>
      <p style={{ fontSize: '0.8rem', marginTop: '0.25rem' }}>{duration}</p>

      {audio && (
        <>
          <audio ref={audioRef} src={audio} />
          <button
            onClick={togglePlay}
            style={{
              position: 'absolute',
              bottom: '1rem',
              right: '1rem',
              background: '#22c55e',
              border: 'none',
              borderRadius: '50%',
              width: '35px',
              height: '35px',
              color: '#111',
              fontWeight: 'bold',
              cursor: 'pointer'
            }}
            title="Lire l'extrait"
          >
            ▶
          </button>
        </>
      )}
    </div>
  );
};

export default MusicCard;
