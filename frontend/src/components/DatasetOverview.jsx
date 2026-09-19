function DatasetOverview({ profile }) {
    return (
        <section className="overview-card">
            <h2>Dataset Overview</h2>

            <div className="overview-stats">
                <div className="stat">
                    <strong>{profile.rows.toLocaleString()}</strong>
                    <span>Rows</span>
                </div>

                <div className="stat">
                    <strong>{profile.columns}</strong>
                    <span>Columns</span>
                </div>
            </div>

            <div className="column-info">
                <p>
                    <strong>Numeric</strong>
                    <span>
                        {profile.numeric_columns.join(", ") || "None"}
                    </span>
                </p>

                <p>
                    <strong>Categorical</strong>
                    <span>
                        {profile.categorical_columns.join(", ") || "None"}
                    </span>
                </p>

                <p>
                    <strong>Date</strong>
                    <span>
                        {profile.date_columns.join(", ") || "None"}
                    </span>
                </p>
            </div>
        </section>
    );
}

export default DatasetOverview;