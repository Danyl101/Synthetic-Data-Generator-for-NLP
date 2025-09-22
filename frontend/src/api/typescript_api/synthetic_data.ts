export const synthetic_data_run = async() =>{
    try{
        const response=await fetch(
            "http://localhost:5000/api/run-synthetic_data",
        {  
            method:"POST",
            headers:{"Content-Type":"Application/json"},
        })
        if(!response.ok)
        {
            throw new Error(`Response not acquired from frontend ${response.status}`)
        }
        const action=await response.json()
        return action
    }
    catch(err:any)
    {
        console.log(`Execution failed during synthetic data api ${err.message}`,err)
        throw new err
    }
}


