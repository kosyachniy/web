import Link from 'next/link';
import { useSelector } from 'react-redux';

export default () => {
  const main = useSelector(state => state.main);

  return (
    <footer className={`bg-${main.theme} ${main.theme === 'dark' ? '' : 'text-muted'} pt-3`}>
      <div className="container d-flex flex-wrap justify-content-between align-items-center py-3 mt-4 border-top">
        <p className="col-md-4 mb-0">
          { process.env.NEXT_PUBLIC_NAME }
          {' '}
          &copy; 2018-
          { new Date().getFullYear() }
        </p>
        <Link href="/" className="col-md-4 d-flex align-items-center justify-content-center mb-md-0 me-md-auto link-dark text-decoration-none">
          <img
            src={`/brand/logo_${main.color}.svg`}
            alt={process.env.NEXT_PUBLIC_NAME}
            style={{ height: '24px' }}
          />
        </Link>
        <ul className="nav col-md-4 justify-content-end list-unstyled d-flex">
          <li className="ms-3 d-flex">
            <Link href="https://t.me/hnklny">
              { main.locale === 'ru' ? 'Канал в Telegram' : 'Telegram Channel' }
            </Link>
          </li>
        </ul>
      </div>
    </footer>
  );
};
