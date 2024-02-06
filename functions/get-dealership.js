const express = require('express')
const app = express()
const port = process.env.PORT || 3000
const Cloudant = require('@cloudant/cloudant')

async function dbCloudantConnect(){
    try{
        const cloudant = Cloudant({
            plugins: {iamauth:{iamApiKey: 'esNNutBwLBLIqnOnI45mGN8_9gU1TntBDqQn5UUvu4Fe'}},
            url: 'https://e180e269-df92-4b84-920f-cda77fa52196-bluemix.cloudantnosqldb.appdomain.cloud'
        })

        const db = cloudant.use('dealerships')
        console.info('Connect Success! Connected to DB')
        return db
    }catch(err){
        console.error('Connect Failure: ' +err.message + ' for Cloudant DB' )
        throw err
    }
}

let db

(async () => {
    db = await dbCloudantConnect()
})()

app.use(express.json())

app.get('/dealerships/get',(req,res) => {
    const {state, id} = req.query

    const selector = {}

    if(state){
        selector.state = state
    }

    if(id){
        selector.id = parseInt(id)
    }

    const queryOptions = {
        selector,
        limit: 10
    }

    db.find(queryOptions,(err,body) => {
        if(err){
            console.log('Error Fetching Dealerships: ',err)
            res.status(500).json({error: 'An error Occurred while fetching dealerships.'})
        }else{
            const dealerships = body.docs
            res.json(dealerships)
        }
    })
})

app.listen(port,() => {
    console.log(`Server is Running on port ${port}`)
})