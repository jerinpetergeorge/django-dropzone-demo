Dropzone.autoDiscover = false;
const myDropzone = new Dropzone('#my-dropzone', {
    url: 'upload/',
    maxFiles: 5,
    acceptedFiles: '.jpg',
    forceChunking: true,
    chunking: true,
})