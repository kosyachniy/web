import Link from 'next/link';

export default ({ page, lastPage, prefix = '' }) => (
  <>
    { lastPage > 1 && (
    <ul className="pagination mb-0">
      { page > 1 && (
      <li className="page-item">
        <Link className="page-link" href={`${prefix}?page=1`}>«</Link>
      </li>
      ) }
      { page > 1 && (
      <li className="page-item">
        <Link className="page-link" href={`${prefix}?page=${page - 1}`}>‹</Link>
      </li>
      ) }
      { page > 2 && (
      <li className="page-item">
        <Link className="page-link" href={`${prefix}?page=${page - 2}`}>{ page - 2 }</Link>
      </li>
      ) }
      { page > 1 && (
      <li className="page-item">
        <Link className="page-link" href={`${prefix}?page=${page - 1}`}>{ page - 1 }</Link>
      </li>
      ) }
      <li className="page-item">
        <Link className="page-link disabled" href={`${prefix}?page=${page}`}>{ page }</Link>
      </li>
      { page < lastPage && (
      <li className="page-item">
        <Link className="page-link" href={`${prefix}?page=${page + 1}`}>{ page + 1 }</Link>
      </li>
      ) }
      { page < lastPage - 1 && (
      <li className="page-item">
        <Link className="page-link" href={`${prefix}?page=${page + 2}`}>{ page + 2 }</Link>
      </li>
      ) }
      { page < lastPage && (
      <li className="page-item">
        <Link className="page-link" href={`${prefix}?page=${page + 1}`}>›</Link>
      </li>
      ) }
      { page < lastPage && (
      <li className="page-item">
        <Link className="page-link" href={`${prefix}?page=${lastPage}`}>»</Link>
      </li>
      ) }
    </ul>
    ) }
  </>
);
