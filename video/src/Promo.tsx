import {AbsoluteFill, Img, OffthreadVideo, Sequence, interpolate, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {loadFont} from '@remotion/google-fonts/Poppins';

const {fontFamily} = loadFont('normal', {weights: ['400', '600', '700'], subsets: ['latin']});

// Brand colours mirror tailwind.config.js.
const FOREST = '#2C4A3B';
const FOREST_DARK = '#1B2F26';
const GOLD = '#B98A46';
const GOLD_LIGHT = '#CDAB7A';
const PAPER = '#FBF9F2';

const sceneSchema = z.object({
  startSec: z.number(),
  durationSec: z.number(),
  // Role label shown as a lower-third chip (swap for real names).
  speaker: z.string().optional(),
  caption: z.string().optional(),
});

export const promoSchema = z.object({
  title: z.string(),
  tagline: z.string(),
  scenes: z.array(sceneSchema),
  partners: z.array(z.string()),
  contact: z.array(z.string()),
  partnersStartSec: z.number(),
  endCardStartSec: z.number(),
});

export type PromoProps = z.infer<typeof promoSchema>;

export const PROMO_FPS = 30;
export const PROMO_DURATION_SEC = 45;

export const promoDefaultProps: PromoProps = {
  title: 'AfraViva Media – Your Partner for Life',
  tagline: 'Faith. Family. Life. Africa.',
  scenes: [
    {startSec: 4, durationSec: 3, speaker: 'Host', caption: 'Good morning, Africa! Come behind the scenes with us.'},
    {startSec: 7, durationSec: 5, speaker: 'Producer', caption: 'High-quality video and audio for TV, web and social media. We are ready when you are.'},
    {startSec: 12, durationSec: 7, speaker: 'Podcast Host', caption: 'Ask honestly, listen well, and let Africa speak for itself.'},
    {startSec: 19, durationSec: 7, speaker: 'Editor', caption: 'Editing, colour grading and post-production: hours of raw footage shaped into something that inspires.'},
    {startSec: 26, durationSec: 7, speaker: 'Strategist', caption: 'Digital marketing, social media and media training, so your message lands with clarity and impact.'},
  ],
  partners: ['Veni Foras', 'The Letter House', 'LifeSite', 'Pro Vita & Famiglia'],
  contact: ['0795 961 943', 'afravivamedia@gmail.com', 'TikTok: afraviva media', 'YouTube: AfravivaMedia', 'St Joseph House, Ngong Road'],
  partnersStartSec: 33,
  endCardStartSec: 38,
};

const useFade = (durationInFrames: number, fade = 8) => {
  const frame = useCurrentFrame();
  return interpolate(frame, [0, fade, durationInFrames - fade, durationInFrames], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
};

const SceneOverlay: React.FC<{speaker?: string; caption?: string; durationInFrames: number}> = ({speaker, caption, durationInFrames}) => {
  const opacity = useFade(durationInFrames);
  return (
    <AbsoluteFill style={{opacity}}>
      {speaker ? (
        <div
          style={{
            position: 'absolute',
            left: 60,
            top: 60 + 882 - 90,
            background: GOLD,
            color: FOREST_DARK,
            fontWeight: 700,
            fontSize: 34,
            padding: '8px 28px',
            borderRadius: 3,
          }}
        >
          {speaker}
        </div>
      ) : null}
      {caption ? (
        <div
          style={{
            position: 'absolute',
            left: 80,
            right: 80,
            top: 60 + 882,
            height: 138,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            textAlign: 'center',
            color: PAPER,
            fontSize: 38,
            lineHeight: 1.3,
          }}
        >
          {caption}
        </div>
      ) : null}
    </AbsoluteFill>
  );
};

const TitleCard: React.FC<{title: string; tagline: string; durationInFrames: number}> = ({title, tagline, durationInFrames}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const opacity = useFade(durationInFrames, 10);
  const rise = spring({frame, fps, config: {damping: 200}});
  return (
    <AbsoluteFill style={{opacity, justifyContent: 'center', alignItems: 'center', background: 'rgba(27,47,38,0.55)'}}>
      <div style={{transform: `translateY(${(1 - rise) * 30}px)`, textAlign: 'center'}}>
        <div style={{color: PAPER, fontSize: 84, fontWeight: 700}}>{title}</div>
        <div style={{color: GOLD_LIGHT, fontSize: 48, marginTop: 20}}>{tagline}</div>
      </div>
    </AbsoluteFill>
  );
};

const Partners: React.FC<{partners: string[]; durationInFrames: number}> = ({partners, durationInFrames}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const opacity = useFade(durationInFrames, 10);
  return (
    <AbsoluteFill style={{opacity, background: FOREST_DARK, justifyContent: 'center', alignItems: 'center'}}>
      <div style={{color: GOLD_LIGHT, fontSize: 40, marginBottom: 40}}>Proud to work in partnership with</div>
      <div style={{display: 'flex', gap: 40}}>
        {partners.map((p, i) => {
          const s = spring({frame: frame - 8 - i * 6, fps, config: {damping: 200}});
          return (
            <div
              key={p}
              style={{
                opacity: s,
                transform: `translateY(${(1 - s) * 24}px)`,
                color: PAPER,
                fontSize: 40,
                fontWeight: 600,
                border: `2px solid ${GOLD}`,
                borderRadius: 3,
                padding: '24px 36px',
              }}
            >
              {p}
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const EndCard: React.FC<{contact: string[]; tagline: string; durationInFrames: number}> = ({contact, tagline, durationInFrames}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const logo = spring({frame, fps, config: {damping: 200}});
  const fadeIn = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  const fadeOut = interpolate(frame, [durationInFrames - 15, durationInFrames], [1, 0], {extrapolateLeft: 'clamp'});
  return (
    <AbsoluteFill style={{opacity: fadeIn * fadeOut, background: FOREST, justifyContent: 'center', alignItems: 'center'}}>
      <Img src={staticFile('img/afraviva-logo.png')} style={{height: 200, transform: `scale(${logo})`}} />
      <div style={{color: PAPER, fontSize: 64, fontWeight: 700, marginTop: 24}}>We tell Africa&apos;s story!</div>
      <div style={{color: GOLD_LIGHT, fontSize: 36, marginTop: 8}}>{tagline}</div>
      <div style={{marginTop: 40, textAlign: 'center', color: PAPER, fontSize: 34, lineHeight: 1.6}}>
        {contact.map((c) => (
          <div key={c}>{c}</div>
        ))}
      </div>
    </AbsoluteFill>
  );
};

export const Promo: React.FC<PromoProps> = ({title, tagline, scenes, partners, contact, partnersStartSec, endCardStartSec}) => {
  const {fps, durationInFrames} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  return (
    <AbsoluteFill style={{background: FOREST_DARK, fontFamily}}>
      {/* Source footage is 1280x588, scaled to full width and letterboxed. */}
      <div style={{position: 'absolute', left: 0, top: 60, width: 1920, height: 882, overflow: 'hidden'}}>
        <OffthreadVideo src={staticFile('video/media-hero.mp4')} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
      </div>

      <Sequence from={0} durationInFrames={f(4)}>
        <TitleCard title={title} tagline={tagline} durationInFrames={f(4)} />
      </Sequence>

      {scenes.map((s) => (
        <Sequence key={s.startSec} from={f(s.startSec)} durationInFrames={f(s.durationSec)}>
          <SceneOverlay speaker={s.speaker} caption={s.caption} durationInFrames={f(s.durationSec)} />
        </Sequence>
      ))}

      <Sequence from={f(partnersStartSec)} durationInFrames={f(endCardStartSec - partnersStartSec)}>
        <Partners partners={partners} durationInFrames={f(endCardStartSec - partnersStartSec)} />
      </Sequence>

      <Sequence from={f(endCardStartSec)} durationInFrames={durationInFrames - f(endCardStartSec)}>
        <EndCard contact={contact} tagline={tagline} durationInFrames={durationInFrames - f(endCardStartSec)} />
      </Sequence>
    </AbsoluteFill>
  );
};
