import {
    BarChart,
    Bar,
    LineChart,
    Line,
    ScatterChart,
    Scatter,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    ResponsiveContainer,
} from "recharts";

function EvidenceChart({ chart }) {
    if (!chart) {
        return null;
    }

    const renderChart = () => {
        if (chart.type === "bar") {
            return (
                <BarChart data={chart.data}>
                    <CartesianGrid strokeDasharray="3 3" />

                    <XAxis dataKey={chart.xKey} />

                    <YAxis />

                    <Tooltip />

                    <Bar dataKey={chart.yKey} />
                </BarChart>
            );
        }

        if (chart.type === "line") {
            return (
                <LineChart data={chart.data}>
                    <CartesianGrid strokeDasharray="3 3" />

                    <XAxis dataKey={chart.xKey} />

                    <YAxis />

                    <Tooltip />

                    <Line
                        type="monotone"
                        dataKey={chart.yKey}
                    />
                </LineChart>
            );
        }

        if (chart.type === "scatter") {
            return (
                <ScatterChart>
                    <CartesianGrid strokeDasharray="3 3" />

                    <XAxis
                        type="number"
                        dataKey={chart.columnA}
                    />

                    <YAxis
                        type="number"
                        dataKey={chart.columnB}
                    />

                    <Tooltip />

                    <Scatter data={chart.data} />
                </ScatterChart>
            );
        }

        return null;
    };

    return (
        <div className="evidence-card">
            <h3>{chart.title}</h3>

            <div className="chart-container">
                <ResponsiveContainer>
                    {renderChart()}
                </ResponsiveContainer>
            </div>
        </div>
    );
}

export default EvidenceChart;