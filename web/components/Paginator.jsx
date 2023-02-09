import Link from 'next/link';

export default ({ page, lastPage }) => (
  <>
    { lastPage > 1 && (
    <ul className="pagination mb-0">
      { page > 1 && (
      <li className="page-item">
        <Link className="page-link" href="?page=1">«</Link>
      </li>
      ) }
      { page > 1 && (
      <li className="page-item">
        <Link className="page-link" href={`?page=${page - 1}`}>‹</Link>
      </li>
      ) }
      { page > 2 && (
      <li className="page-item">
        <Link className="page-link" href={`?page=${page - 2}`}>{ page - 2 }</Link>
      </li>
      ) }
      { page > 1 && (
      <li className="page-item">
        <Link className="page-link" href={`?page=${page - 1}`}>{ page - 1 }</Link>
      </li>
      ) }
      <li className="page-item">
        <Link className="page-link disabled" href={`?page=${page}`}>{ page }</Link>
      </li>
      { page < lastPage && (
      <li className="page-item">
        <Link className="page-link" href={`?page=${page + 1}`}>{ page + 1 }</Link>
      </li>
      ) }
      { page < lastPage - 1 && (
      <li className="page-item">
        <Link className="page-link" href={`?page=${page + 2}`}>{ page + 2 }</Link>
      </li>
      ) }
      { page < lastPage && (
      <li className="page-item">
        <Link className="page-link" href={`?page=${page + 1}`}>›</Link>
      </li>
      ) }
      { page < lastPage && (
      <li className="page-item">
        <Link className="page-link" href={`?page=${lastPage}`}>»</Link>
      </li>
      ) }
    </ul>
    ) }
  </>
);
