import { useEffect } from 'react';
import { useTranslation } from 'next-i18next';

const Toast = ({
  header, text, color = 'black', background = 'light',
}) => {
  const { t } = useTranslation('common');

  useEffect(() => {
    const toastList = [].slice.call(document.querySelectorAll('.toast'));
    new bootstrap.Toast(toastList.pop(), { delay: 2000 }).show(); /* eslint-disable-line */
  }, []);

  return (
    <div
      className={`toast mt-3 text-${color} bg-${background} border-0`}
      role="alert"
      aria-live="assertive"
      aria-atomic="true"
    >
      <div className={`toast-header text-${color} bg-${background}`}>
        <strong className="me-auto">{ header }</strong>
        <small>{ t('system.now') }</small>
        <button
          type="button"
          className="btn-close"
          data-bs-dismiss="toast"
          aria-label="Close"
        />
      </div>
      <div className="toast-body">{ text }</div>
    </div>
  );
};

export default ({ toasts }) => (
  <div
    className="position-fixed bottom-0 end-0 p-3"
    style={{ zIndex: 5000 }}
  >
    { toasts.map((toast, i) => <Toast {...toast} key={i} />) }
  </div>
);
