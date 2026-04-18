import { useState } from "react";
import API from "../api";

export default function Upload() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const uploadFile = async () => {
    if (!file) {
      alert("Please select a file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await API.post("/upload/", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });

      setResult(res.data);
    } catch (err) {
      console.error(err);
      alert("Upload failed");
    }
  };

  const createCandidate = async () => {
    await API.post(`/candidate/?name=Test&email=test@gmail.com`);
    alert("Candidate saved");
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Upload Resume</h2>

      <input
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <br /><br />

      <button onClick={uploadFile}>Upload</button>
      <button onClick={createCandidate} style={{ marginLeft: 10 }}>
        Save Candidate
      </button>

      {result && (
        <div style={{ marginTop: 20 }}>
          <p><b>Score:</b> {result.score}</p>
          <p><b>Decision:</b> {result.decision}</p>
        </div>
      )}
    </div>
  );
}