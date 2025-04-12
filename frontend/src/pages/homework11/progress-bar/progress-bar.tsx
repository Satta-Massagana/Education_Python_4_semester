import { useState, useEffect } from 'react';

const ProgressBar = () => {
  const [progress, setProgress] = useState(0);
  const [isComplete, setIsComplete] = useState(false);

  useEffect(() => {
    const totalDuration = 5000; // 5 секунд
    const intervalTime = 1000; // Обновлять каждую секунду
    const increment = 100 / (totalDuration / intervalTime); // 20% за шаг

    const timer = setInterval(() => {
      setProgress(prevProgress => {
        const newProgress = prevProgress + increment;
        if (newProgress >= 100) {
          clearInterval(timer);
          setIsComplete(true);
          return 100;
        }

        return newProgress;
      });
    }, intervalTime);

    return () => clearInterval(timer);
  }, []);

  return (
    <div style={{ maxWidth: '500px', margin: '20px auto' }}>
      <h2>Прогресс выполнения задачи</h2>
      <div 
        style={{
          height: '30px',
          backgroundColor: '#e0e0e0',
          borderRadius: '5px',
          marginBottom: '10px'
        }}
      >
        <div
          style={{
            width: `${progress}%`,
            height: '100%',
            backgroundColor: '#4caf50',
            borderRadius: '5px',
            transition: 'width 0.3s ease'
          }}
        />
      </div>
      <div style={{ textAlign: 'center' }}>
        {isComplete ? (
          <p style={{ color: '#4caf50', fontWeight: 'bold' }}>Готово!</p>
        ) : (
          <p>{Math.round(progress)}%</p>
        )}
      </div>
    </div>
  );
};

export default ProgressBar;
