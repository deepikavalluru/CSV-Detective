function getInvestigationLabel(tool) {
    const labels = {
        profile_dataset: "Dataset profiled",
        get_top_values: "Top values analyzed",
        compare_groups: "Groups compared",
        calculate_correlation: "Relationships analyzed",
        analyze_trend: "Trends analyzed",
        detect_anomalies: "Anomalies detected",
    };

    return labels[tool] || "Data analyzed";
}

function Investigation({ investigation }) {
    return (
        <section>
            <h2>Investigation</h2>

            <div className="investigation-list">
                {investigation.map((step, index) => (
                    <div
                        className="investigation-step"
                        key={index}
                    >
                        <span className="investigation-status">
                            {step.status === "completed" ? "✓" : "!"}
                        </span>

                        <span>
                            {getInvestigationLabel(step.tool)}
                        </span>
                    </div>
                ))}
            </div>
        </section>
    );
}

export default Investigation;