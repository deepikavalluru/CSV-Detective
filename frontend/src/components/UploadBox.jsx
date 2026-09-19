function UploadBox({ onFileSelect }) {
  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];

    if (!selectedFile) {
      return;
    }

    if (!selectedFile.name.endsWith(".csv")) {
      alert("Please select a CSV file.");
      return;
    }

    onFileSelect(selectedFile);
  };

  return (
    <div>
      <h2>Upload your CSV</h2>

      <input
        type="file"
        accept=".csv"
        onChange={handleFileChange}
      />
    </div>
  );
}

export default UploadBox;