import Card from './Card'


export default ({ posts }) => (
    <div className="album py-2">
        <div className="row">
            { posts.map((el, num) =>
                <Card post={ el } key={ num } />
            ) }
        </div>
    </div>
)