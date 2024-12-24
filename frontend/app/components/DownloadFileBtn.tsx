import { downloadFile } from '../lib/api';

function FileDownloadButton({ fileId }: { fileId: number }) {
    const handleDownload = async () => {
        try {
            await downloadFile(fileId);

        } catch (error) {
            console.error('Error downloading file:', error);
        }
    };

    return (
        <button
            onClick={handleDownload}
            className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-green-500 focus:ring-opacity-50"
        >
            Download File
        </button>
    );
}

export default FileDownloadButton;
