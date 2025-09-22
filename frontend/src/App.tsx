"use client"

import { addfilter, addsite } from "api/typescript_api/add_api"
import { removefilter, removesite } from "api/typescript_api/remove_api"
import { scrape_run, extract_run } from "api/typescript_api/programs_run"
import { synthetic_data_run } from "api/typescript_api/synthetic_data"

import { FilterSiteInput } from "components/FilterSiteInput"
import { RunButtons } from "components/RunButtons"
import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "components/ui/card"
import { Settings, Database, Globe ,Play,List,BarChart } from "lucide-react"


import { Line } from "react-chartjs-2";
import { Chart as ChartJS, Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale } from "chart.js"

ChartJS.register(Title, Tooltip, Legend, LineElement, PointElement, CategoryScale, LinearScale);

export default function App() {
  const [list, setList] = useState<string[]>([])
  const [input, setInput] = useState<string>("")

  const filteradd = async (input : string) => {
    try {
      const res = await addfilter([input])
      console.log("Filter added API Response", res)
    } catch (err) {
      console.error("Filter add failed", err)
    }
  }

  const siteadd = async (input :string) => {
    try {
      const res = await addsite([input])
      console.log("Site added API Response", res)
    } catch (err) {
      console.error("Site add failed", err)
    }
  }

  const filterremove = async (input :string) => {
    try {
      const res = await removefilter([input])
      console.log("Remove Filter API Response", res)
    } catch (err) {
      console.log("Filter removal failed", err)
    }
  }

  const siteremove = async (input :string) => {
    try {
      const res = await removesite([input])
      console.log("Remove Site API Response", res)
    } catch (err) {
      console.log("Filter removal failed", err)
    }
  }

  // ---- Actions for RunButtons ----
  const actions = [
    { label: "Scrape", icon: <Play className="h-5 w-5 mr-2" />, action: scrape_run },
    { label: "Extract", icon: <List className="h-5 w-5 mr-2" />, action: extract_run },
    { label: "Synthetic Data Generation", icon: <BarChart className="h-5 w-5 mr-2" />, action: synthetic_data_run },
  ]

  // ---- UI Layout ----
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 to-slate-100 p-4">
      <div className="max-w-4xl mx-auto space-y-8">
        {/* Header */}
        <div className="text-center space-y-2">
          <div className="flex items-center justify-center gap-2 mb-4">
            <Settings className="h-8 w-8 text-primary" />
            <h1 className="text-4xl font-bold tracking-tight">Scraper Control Panel</h1>
          </div>
          <p className="text-muted-foreground text-lg">
            Manage your web scraping filters, sites, and operations
          </p>
        </div>

        {/* Filter + Site Management */}
        <div className="grid gap-6 md:grid-cols-2">
          <Card className="shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Database className="h-5 w-5" />
                Filter Management
              </CardTitle>
              <CardDescription>
                Add or remove filters to control what content gets scraped
              </CardDescription>
            </CardHeader>
            <CardContent>
              <FilterSiteInput
                label="Filter"
                onAdd={filteradd}
                onRemove={filterremove}
                disabled={false}
              />
            </CardContent>
          </Card>

          <Card className="shadow-lg">
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <Globe className="h-5 w-5" />
                Site Management
              </CardTitle>
              <CardDescription>
                Add or remove websites from your scraping targets
              </CardDescription>
            </CardHeader>
            <CardContent>
              <FilterSiteInput
                label="Site"
                onAdd={siteadd}
                onRemove={siteremove}
                disabled={false}
              />
            </CardContent>
          </Card>
        </div>

        {/* Operations */}
        <section>
          <Card className="shadow-lg">
            <CardHeader>
              <CardTitle className="text-center">Operations</CardTitle>
              <CardDescription className="text-center">
                Run scraping pipeline
              </CardDescription>
            </CardHeader>
            <CardContent>
              <RunButtons actions={actions} disabled={false} />
            </CardContent>
          </Card>
        </section>
      </div>
    </div>
  )
}

interface GraphsProps{
  predictions:number[]
}

export function PredictionGraph({predictions}:GraphsProps) {
  const data = {
    labels: predictions.map((_, i) => i + 1),
    datasets: [
      {
        label:"Predictions",
        data:predictions,
        borderColor:"rgb(75,192,192)",
        fill:false
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "top" as const },
      title: { display: true, text: "Stock Price Trend" },
    },
  };

  return <Line data={data} options={options} />;
}
