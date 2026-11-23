import { GoogleGenAI } from '@google/genai';
import fs from 'fs';

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
const reqText = fs.readFileSync('../docs/requirements.md', 'utf-8');

const start = performance.now();
const response = await ai.models.generateContent({
  model: 'gemini-2.5-flash',
  contents: `Перевір, чи всі нефункціональні вимоги в цьому документі мають вимірювані показники. Відповідай стисло українською:\n${reqText}`
});
const elapsed = ((performance.now() - start) / 1000).toFixed(2);

console.log(response.text);
console.log(`\nProvider: Google AI Studio | Model: gemini-2.5-flash | Time: ${elapsed} s`);