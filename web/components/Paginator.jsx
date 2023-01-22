import { useSelector } from 'react-redux'


export default ({ page, lastPage }) => {
    const main = useSelector(state => state.main)

    return (
        <>
            { lastPage > 1 && (
                <ul className="pagination mb-0">
                    { page > 1 && (
                        <li className="page-item">
                            <a className={ `page-link bg-${main.theme}` } href="?page=1">«</a>
                        </li>
                    ) }
                    { page > 1 && (
                        <li className="page-item">
                            <a className={ `page-link bg-${main.theme}` } href={ `?page=${page-1}` }>‹</a>
                        </li>
                    ) }
                    { page > 2 && (
                        <li className="page-item">
                            <a className={ `page-link bg-${main.theme}` } href={ `?page=${page-2}` }>{ page - 2 }</a>
                        </li>
                    ) }
                    { page > 1 && (
                        <li className="page-item">
                            <a className={ `page-link bg-${main.theme}` } href={ `?page=${page-1}` }>{ page - 1 }</a>
                        </li>
                    ) }
                    <li className="page-item">
                        <a className={ `page-link bg-${main.theme} disabled` } href={ `?page=${page}` }>{ page }</a>
                    </li>
                    { page < lastPage && (
                        <li className="page-item">
                            <a className={ `page-link bg-${main.theme}` } href={ `?page=${page+1}` }>{ page + 1 }</a>
                        </li>
                    ) }
                    { page < lastPage -1 && (
                        <li className="page-item">
                            <a className={ `page-link bg-${main.theme}` } href={ `?page=${page+2}` }>{ page + 2 }</a>
                        </li>
                    ) }
                    { page < lastPage && (
                        <li className="page-item">
                            <a className={ `page-link bg-${main.theme}` } href={ `?page=${page+1}` }>›</a>
                        </li>
                    ) }
                    { page < lastPage && (
                        <li className="page-item">
                            <a className={ `page-link bg-${main.theme}` } href={ `?page=${lastPage}` }>»</a>
                        </li>
                    ) }
                </ul>
            ) }
        </>
    )
}
