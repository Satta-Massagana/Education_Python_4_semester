export function fetchData(url: string) {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // Имитация разных ответов для разных URL
      if (url === '/api/users') {
        resolve({
          users: [
            { id: 1, name: 'Иван Иванов', profileUrl: '/api/users/1' },
            { id: 2, name: 'Петр Петров', profileUrl: '/api/users/2' }
          ]
        });
      } else if (url.startsWith('/api/users/')) {
        const userId = url.split('/').pop();
        resolve({
          id: userId,
          name: userId === '1' ? 'Иван Иванов' : 'Петр Петров',
          age: userId === '1' ? 30 : 25,
          email: userId === '1' ? 'ivan@example.com' : 'petr@example.com'
        });
      } else {
        reject(new Error('Неверный URL запроса'));
      }
    }, 2000);
  });
}
