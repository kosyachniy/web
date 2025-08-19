import Card from './Card';

export default ({ posts }) => (
  <div className="album py-2">
    <div className="row">
      { posts.map((el, num) => (
        <div className="col-md-4" key={num}>
          <Card post={el} />
        </div>
      )) }
    </div>
  </div>
);
