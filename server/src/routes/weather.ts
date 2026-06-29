import { Router, Request, Response } from 'express';
import { z } from 'zod';
import { getStates } from '../lib/openai.js';
import { fetchHourlyWeather } from '../lib/weather.js';
import { generateWeatherSummary } from '../lib/openai.js';
import { WeatherResponse } from '../types.js';

const router = Router();

const querySchema = z.object({
  state: z.string().min(1, 'State parameter is required'),
});

router.get('/', async (req: Request, res: Response) => {
  const parsed = querySchema.safeParse(req.query);
  if (!parsed.success) {
    res.status(400).json({
      error: 'Validation failed',
      details: parsed.error.flatten().fieldErrors,
    });
    return;
  }

  const { state } = parsed.data;
  const stateKey = state.toUpperCase();

  const states = await getStates();
  const stateInfo = states.find(
    (s) => s.abbreviation === stateKey || s.name.toLowerCase() === state.toLowerCase()
  );

  if (!stateInfo) {
    res.status(404).json({ error: `State "${state}" not found` });
    return;
  }

  try {
    const hourly = await fetchHourlyWeather(stateInfo.latitude, stateInfo.longitude);

    const summary = await generateWeatherSummary(
      stateInfo.name,
      stateInfo.capital,
      hourly,
    );

    const response: WeatherResponse = {
      state: stateInfo,
      current: hourly[0]!,
      hourly,
      summary,
      updatedAt: new Date().toISOString(),
    };

    res.set('Cache-Control', 'public, max-age=300');
    res.json(response);
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown error';
    res.status(502).json({ error: 'Failed to fetch weather data', details: message });
  }
});

export default router;
