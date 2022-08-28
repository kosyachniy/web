import S3 from 'react-aws-s3'

import { generete } from './token'


const ReactS3Client = new S3({
    bucketName: process.env.NEXT_PUBLIC_AMAZON_BUCKET_NAME,
    dirName: process.env.NEXT_PUBLIC_AMAZON_DIR_NAME,
    region: process.env.NEXT_PUBLIC_AMAZON_REGION,
    accessKeyId: process.env.NEXT_PUBLIC_AMAZON_ID,
    secretAccessKey: process.env.NEXT_PUBLIC_AMAZON_SECRET,
});


export default function uploadImage(fileInput) {
    return new Promise((resolve) => {
        ReactS3Client.uploadFile(fileInput, generete()).then((data) => {
            if (data.status === 204) {
                resolve(data.location);
            } else {
                resolve('');
            }
        });
    });
}
