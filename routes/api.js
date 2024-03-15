const express = require('express');
const router = express.Router();
const axios = require('axios');
const { exec } = require('child_process');
const openaiService = require('../services/openaiService.js');

router.get('/news', async (req, res) => {
	exec('python3 ./scripts/news.py', async (err, stdout, stderr) => {
		console.log(`stdout: ${stdout}`);
		console.log(`stderr: ${stderr}`);
		if (err) {
			return res.status(500).json({result: `${stderr}` });
		}else{
			const prompt = `Which Korean TV shows and movies were mentioned the most in the past month in the news?:  \n\n${stdout}`;			
			// Alternatively, the promt can be combined with the JSON file data:
			// const news_data = JSON.parse(fs.readFileSync('./retrieved-info.json', 'utf8'));
			// const question = "Which Korean TV shows and movies were mentioned the most in the past month in the news?"
			// const promt = question + JSON.stringify(news_data);
			const gptRespJson = await openaiService.chat(prompt)
				.then((gptRespJson) => {
					//console.log("gptRespJson: ", gptRespJson);
					if(gptRespJson.GPTstatus==200){
						return res.status(200).json({result: gptRespJson.reply});
					}else{
						return res.status(gptRespJson.GPTstatus).json({result: gptRespJson});
					}
				}).catch((error) => {
					return res.status(500).json({error: error});
				});
		}
	});
});

router.get('/test', (req, res) => {
	return res.status(200).json({result: "TEST" });
});

module.exports = router;