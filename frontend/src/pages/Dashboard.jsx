import { useState } from "react";
import UploadBox from "../components/UploadBox";
import DatasetOverview from "../components/DatasetOverview";
import Investigation from "../components/Investigation";
import FindingCard from "../components/FindingCard";
import EvidenceChart from "../components/EvidenceChart";
import { investigateCSV } from "../services/api";

function Dashboard() {
    const [file, setFile] = useState(null);
    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleAnalyze = async () => {
        if (!file) {
            return;
        }

        try {
            setLoading(true);
            setError(null);
            setResult(null);

            const data = await investigateCSV(file);

            setResult(data);
        } catch (error) {
            console.error(error);

            setError(
                error.response?.data?.detail ||
                "Failed to analyze CSV."
            );
        } finally {
            setLoading(false);
        }
    };

    return (
        <main className="dashboard">
            <header className="hero">
                <p className="eyebrow">AI DATA INVESTIGATION</p>

                <h1>CSV Detective</h1>

                <p className="subtitle">
                    Upload a CSV and let AI investigate the data,
                    uncover findings, and show the evidence.
                </p>
            </header>

            <section className="upload-section">
                <UploadBox onFileSelect={setFile} />

                {file && (
                    <div className="selected-file">
                        <p>
                            Selected file: <strong>{file.name}</strong>
                        </p>

                        <button
                            className="analyze-button"
                            onClick={handleAnalyze}
                            disabled={loading}
                        >
                            {loading ? (
                                <>
                                    <span className="spinner"></span>
                                    Investigating...
                                </>
                            ) : (
                                "Analyze CSV"
                            )}
</button>
                    </div>
                )}
            </section>

            {error && (
                <section className="error-message">
                    <strong>Investigation failed</strong>
                    <p>{error}</p>
                </section>
            )}

            {result && (
                <div className="results">
                    <DatasetOverview
                        profile={result.profile.results}
                    />

                    <Investigation
                        investigation={result.investigation}
                    />

                    <FindingCard
                        findings={result.findings}
                    />

                    {result.charts?.length > 0 && (
                        <section className="evidence-section">
                            <div className="section-heading">
                                <p className="eyebrow">DATA EVIDENCE</p>
                                <h2>Evidence</h2>
                            </div>

                            {result.charts.map((chart, index) => (
                                <EvidenceChart
                                    key={index}
                                    chart={chart}
                                />
                            ))}
                        </section>
                    )}
                </div>
            )}
        </main>
    );
}

export default Dashboard;