"use client"
import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Alert, AlertDescription } from "@/components/ui/alert"
import { Loader2,CheckCircle, XCircle } from "lucide-react"

interface ActionConfig{
  label:string
  icon:React.ReactNode
  action: ()=>Promise<void>
}

interface RunButtonsProp {
  actions: ActionConfig[]
  disabled: boolean
}

interface Status {
  loading: boolean
  success: boolean | null
  message?: string
}


export function RunButtons({actions,disabled }: RunButtonsProp) {
  const [status, setstatus] = useState<Status[]>(actions.map(()=>({ loading: false, success: null })))

  // Generic runner
  const runAction = async (
    idx : number,
    action: () => Promise<void>,
    label: string,
  ) => {
    const newStatus=[...status]
    newStatus[idx] = { loading: true, success: null }
    setstatus(newStatus)
    try {
      await action()
      newStatus[idx] = { loading: false, success: true, message: `${label} completed successfully` }
      setstatus([...newStatus]) // send back array
    }
    catch (e: any) {
      newStatus[idx] = { loading: false, success: false, message: `${label} failed: ${e.message}` }
      setstatus([...newStatus]) // send back array
    }
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-8 items-center">
        {actions.map((a, idx) => (
          <Button
            key={a.label}
            onClick={() => runAction(idx, a.action, a.label  )}
            disabled={disabled || status[idx].loading}
            size="lg"
            className="!px-4 !py-6 !min-w-[400px] !w-auto "
          >
            {status[idx].loading ? (
              <Loader2 className="h-5 w-5 mr-2 animate-spin" />
            ) : (
              a.icon
            )}
            {`Run ${a.label}`}
          </Button>
        ))}
      </div>

      {/* Alerts */}
      {status.map(
        (s, idx) =>
          s.success !== null && (
            <Alert
              key={idx}
              className={s.success ? "border-green-200 bg-green-50" : "border-red-200 bg-red-50"}
              variant={s.success ? "default" : "destructive"}
            >
              {s.success ? (
                <CheckCircle className="h-4 w-4 text-green-600" />
              ) : (
                <XCircle className="h-4 w-4" />
              )}
              <AlertDescription className={s.success ? "text-green-800" : ""}>
                {s.message}
              </AlertDescription>
            </Alert>
          )
      )}
    </div>
  )
}