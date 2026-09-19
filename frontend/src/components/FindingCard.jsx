import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

function FindingCard({ findings }) {
    const cleanedFindings = findings.replace(/\\\|/g, "|");

    return (
        <section className="findings-card">
            <p className="eyebrow">AI ANALYSIS</p>

            <h2>Findings</h2>

            <div className="findings-content">
                <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {cleanedFindings}
                </ReactMarkdown>
            </div>
        </section>
    );
}

export default FindingCard;