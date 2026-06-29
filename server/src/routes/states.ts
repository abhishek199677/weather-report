import { Router, Request, Response } from 'express';
import { getStates } from '../lib/openai.js';

const router = Router();

router.get('/', async (_req: Request, res: Response) => {
  try {
    const states = await getStates();
    const list = states.map(({ name, abbreviation, capital }) => ({
      name,
      abbreviation,
      capital,
    }));
    res.json(list);
  } catch (error) {
    const message = error instanceof Error ? error.message : 'Unknown error';
    res.status(500).json({ error: 'Failed to load states', details: message });
  }
});

export default router;
