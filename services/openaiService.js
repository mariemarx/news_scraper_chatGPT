const axios = require('axios');

async function chat(prompt) {
    const url = 'https://api.openai.com/v1/chat/completions';

    const config = {
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'INSERT KEY'
        },
        timeout: 5000
    };

    let data = {
        "model": "gpt-3.5-turbo",
        "messages": [{
            "role": "user",
            "content": ""
        }],
        "temperature": 0.7
    };

    data.messages[0].content=prompt;
    try{
        let gptResponse = await axios.post(url,data,config);
        return {GPTstatus: 200, prompt: prompt, reply: gptResponse.data.choices[0].message.content };
    }catch(err){
        const error = err.response?err.response.data:err;
        console.error(`Error calling GPT: `, error);
        return {GPTstatus: 400, prompt: prompt, reply: undefined, error: error};
    }
}

module.exports = {
    chat
}


