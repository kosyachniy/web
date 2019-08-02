import React from 'react'
import { Link } from 'react-router-dom'


export default class Post extends React.Component {
	render() {
		const el = this.props.el

		return (
			<div className="col-md-4">
				<Link to={ '/post/' + el.id } key={ el.id }>
					<div className="card mb-4 shadow-sm">
						{ el.cover && <img className="card-img-top" src={ el.cover } alt={ el.name } /> }
						<div className="card-body">
							<p className="card-text">
								{/* <span className="badge badge-success" style={ marginRight: '10px', fontSize: '15px' }>
									<img src="/static/icon/{{ icon }}.svg">
								</span> */}
								{ el.name }
							</p>

							{ el.description && 
							<div className="d-flex justify-content-between align-items-center">
								{ el.description }
								{/* <div className="btn-group">
									<button type="button" className="btn btn-sm btn-outline-secondary">View</button>
									<button type="button" className="btn btn-sm btn-outline-secondary">Edit</button>
								</div> */}
								{ el.additionally && <small className="text-muted">{ el.additionally }</small> }
							</div>
							}
						</div>
					</div>
				</Link>
			</div>
			// <div>{ ReactHtmlParser(el.cont) }</div>
		)
	}
}