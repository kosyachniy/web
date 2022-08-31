import { useSelector } from 'react-redux'
import Link from 'next/link'

import Card from './Card'


export default ({ posts }) => {
    const system = useSelector((state) => state.system)

    return (
        <>
            <div className="row">
                <div className="col-xs-10 col-sm-10 col-md-10">
                    <div className="btn-group" role="group" >
                        <button
                            type="button"
                            className={`btn btn-${system.theme}`}
                        >
                            <i className="fas fa-th-large"></i>
                        </button>
                        <button
                            type="button"
                            className={`btn btn-${system.theme}`}
                        >
                            <i className="fas fa-th-list"></i>
                        </button>
                        <button
                            type="button"
                            className={`btn btn-${system.theme}`}
                        >
                            <i className="fas fa-image"></i>
                        </button>
                    </div>
                </div>
                <div className="col-xs-2 col-sm-2 col-md-2" style={{ textAlign: 'right' }}>
                    <div className="btn-group">
                        <Link href="/posts/add">
                            <button
                                type="button"
                                className="btn btn-success"
                                style={ {width: '100%'} }
                            >
                                <i className="fas fa-plus" />
                            </button>
                        </Link>
                    </div>
                </div>
            </div>

            <div className="album py-2">
                <div className="row">
                    { posts.map((el, num) =>
                        <Card post={ el } key={ num } />
                    ) }
                </div>
            </div>
        </>
    )
}
