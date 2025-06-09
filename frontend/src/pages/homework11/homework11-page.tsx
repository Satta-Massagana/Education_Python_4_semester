import { FC, useEffect, useRef, useState } from "react";
import "./homework11-page.scss";
import { fetchData } from "./mocks/fetch-data-mock";
import ProgressBar from "./progress-bar/progress-bar";

const Homework11Page: FC = () => {

  const hasRun = useRef(false);
  const [ showProgress, setShowProgress ] = useState(false);
  const [ log, setLog ] = useState<string[]>([]);

  useEffect(() => {
    if (!hasRun.current) {
      hasRun.current = true;
      logMessage('TASK 1');
      task1()
        .then(() => {
          logMessage('TASK 2');
          return task2();
        })
        .then(() => {
          logMessage('TASK 3');
          return task3();
        })
        .then(() => {
          logMessage('TASK 4');
          setShowProgress(true);
        });
    }
  }, []);

  const logMessage = (msg: string) => {
    setLog((prev) => [...prev, msg ]);
  }

  const task1 = () => {
    return new Promise((resolve) => {
      logMessage("1. Начало синхронного кода"); // Синхронный код

      setTimeout(() => {
        logMessage("5. setTimeout - макрозадача"); // Макрозадача (Callback Queue)
        resolve(null);
      }, 0);
  
      Promise.resolve()
        .then(() => {
          logMessage("3. Promise - микрозадача 1"); // Микрозадача (Microtask Queue)
        })
        .then(() => {
          logMessage("4. Promise - микрозадача 2"); // Микрозадача (Microtask Queue)
        });

        logMessage("2. Конец синхронного кода"); // Синхронный код
    })
  }

  const task2 = () => {
    return new Promise((resolve) => {
      fetchData('/api/users')
        .then((response: any) => {
          logMessage('Список пользователей:');
          for(let user of response.users) {
            logMessage(`Пользователь ${user.name}`);
          }
          const firstUserUrl = response.users[0].profileUrl;
          return fetchData(firstUserUrl);
        })
      .then((userInfo: any) => {
        logMessage('Информация о первом пользователе:');
        logMessage(`Имя: ${userInfo.name}`);
        logMessage(`Возраст: ${userInfo.age}`);
        logMessage(`E-mail: ${userInfo.email}`);
        resolve(null);
      })
      .catch(error => {
        logMessage(`Произошла ошибка: ${error.message.toString()}`);
      });
    });
  }

  const task3 = async () => {
      try {
        const response: any = await fetchData('/api/users');
        logMessage('Список пользователей:');
        for(let user of response.users) {
          logMessage(`Пользователь ${user.name}`);
        }
        const firstUserUrl = response.users[0].profileUrl;
        const userInfo: any = await fetchData(firstUserUrl);

        logMessage('Информация о первом пользователе:');
        logMessage(`Имя: ${userInfo.name}`);
        logMessage(`Возраст: ${userInfo.age}`);
        logMessage(`E-mail: ${userInfo.email}`);
      }
      catch(error: any) {
        logMessage(`Произошла ошибка: ${error.message.toString()}`);
      };
  }



  return <div className="app-page">
      <h3>Homework 11</h3>
      <div className="execution-log">
        { log.map((msg, idx) => 
          <div key={ `msg_${idx}` } className="execution-log__message">{msg}</div> )
        }
      </div>
      { showProgress && <ProgressBar /> }
    </div>;
}

export default Homework11Page