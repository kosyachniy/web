import styles from '../../styles/upload.module.css';
import upload from '../../lib/upload';

export default ({ image, setImage }) => {
  const handleUpload = file => upload(file).then(link => setImage(link));

  return (
    <label
      className={styles.upload}
      htmlFor="uploader"
      style={{ border: image ? 0 : null }}
    >
      { image ? (
        <div style={{ backgroundImage: `url(${image})` }} />
      ) : (
        <i className="bi bi-file-earmark-arrow-up" />
      ) }

      <input
        id="uploader"
        type="file"
        accept="image/jpeg, image/png"
        onChange={event => handleUpload(event.target.files[0])}
      />
    </label>
  );
};
