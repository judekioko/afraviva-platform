import {AbsoluteFill, Audio, Img, OffthreadVideo, Sequence, interpolate, random, spring, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {loadFont} from '@remotion/google-fonts/Poppins';

const {fontFamily} = loadFont('normal', {weights: ['400', '600', '700'], subsets: ['latin']});

// Brand colours mirror tailwind.config.js.
const FOREST = '#2C4A3B';
export const FOREST_DARK = '#1B2F26';
const GOLD = '#B98A46';
const GOLD_LIGHT = '#CDAB7A';
const PAPER = '#FBF9F2';

// Layout adapts to the canvas: 16:9 letterboxes the footage, 9:16 (TikTok) crops
// it to a tall window that slowly pans, and keeps text inside TikTok's safe area.
const useLayout = () => {
  const {width, height} = useVideoConfig();
  const vertical = height > width;
  return vertical
    ? {vertical, width, height, vTop: 190, vH: 1110, capTop: 190 + 1110 + 20, capH: 260, capSide: 70, capSize: 50, chipSize: 38, titleSize: 68, taglineSize: 40, partnerSize: 44, logoW: 780, endTitle: 64, endTag: 36, endContact: 36}
    : {vertical, width, height, vTop: 60, vH: 882, capTop: 60 + 882, capH: 138, capSide: 80, capSize: 38, chipSize: 34, titleSize: 84, taglineSize: 48, partnerSize: 40, logoW: 560, endTitle: 56, endTag: 32, endContact: 30};
};

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
  const L = useLayout();
  return (
    <AbsoluteFill style={{opacity}}>
      {speaker ? (
        <div
          style={{
            position: 'absolute',
            left: 60,
            top: L.vTop + L.vH - 90,
            background: GOLD,
            color: FOREST_DARK,
            fontWeight: 700,
            fontSize: L.chipSize,
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
            left: L.capSide,
            right: L.capSide,
            top: L.capTop,
            height: L.capH,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            textAlign: 'center',
            color: PAPER,
            fontSize: L.capSize,
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
  const L = useLayout();
  const rise = spring({frame, fps, config: {damping: 200}});
  return (
    <AbsoluteFill style={{opacity, justifyContent: 'center', alignItems: 'center', background: 'rgba(27,47,38,0.55)'}}>
      <div style={{transform: `translateY(${(1 - rise) * 30}px)`, textAlign: 'center', padding: '0 70px'}}>
        <div style={{color: PAPER, fontSize: L.titleSize, fontWeight: 700}}>{title}</div>
        <div style={{color: GOLD_LIGHT, fontSize: L.taglineSize, marginTop: 20}}>{tagline}</div>
      </div>
    </AbsoluteFill>
  );
};

const Partners: React.FC<{partners: string[]; durationInFrames: number}> = ({partners, durationInFrames}) => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const opacity = useFade(durationInFrames, 10);
  const L = useLayout();
  return (
    <AbsoluteFill style={{opacity, background: FOREST_DARK, justifyContent: 'center', alignItems: 'center'}}>
      <div style={{color: GOLD_LIGHT, fontSize: L.partnerSize, marginBottom: 40, textAlign: 'center'}}>Proud to work in partnership with</div>
      <div style={{display: 'flex', gap: 32, flexWrap: 'wrap', justifyContent: 'center', maxWidth: L.vertical ? 900 : undefined, flexDirection: L.vertical ? 'column' : 'row', alignItems: 'center'}}>
        {partners.map((p, i) => {
          const s = spring({frame: frame - 8 - i * 6, fps, config: {damping: 200}});
          return (
            <div
              key={p}
              style={{
                opacity: s,
                transform: `translateY(${(1 - s) * 24}px)`,
                color: PAPER,
                fontSize: L.partnerSize,
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

const COLS = 10;
const ROWS = 7;

// The logo breaks into tiles that fly in from scattered positions and snap together.
const AssemblingLogo: React.FC<{width: number}> = ({width: LOGO_W}) => {
  const LOGO_H = Math.round((LOGO_W * 493) / 746);
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const tw = LOGO_W / COLS;
  const th = LOGO_H / ROWS;
  const tiles = [];
  for (let r = 0; r < ROWS; r++) {
    for (let c = 0; c < COLS; c++) {
      const id = `${r}-${c}`;
      const delay = 4 + random(`d${id}`) * 28;
      const p = spring({frame: frame - delay, fps, config: {damping: 16, stiffness: 90, mass: 0.9}});
      const dx = (random(`x${id}`) - 0.5) * 1400;
      const dy = (random(`y${id}`) - 0.5) * 900;
      const rot = (random(`r${id}`) - 0.5) * 360;
      const opacity = interpolate(frame - delay, [0, 6], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
      tiles.push(
        <div
          key={id}
          style={{
            position: 'absolute',
            left: c * tw,
            top: r * th,
            // 1px overlap hides seams once the tiles meet.
            width: tw + 1,
            height: th + 1,
            opacity,
            transform: `translate(${(1 - p) * dx}px, ${(1 - p) * dy}px) rotate(${(1 - p) * rot}deg) scale(${0.5 + 0.5 * p})`,
            backgroundImage: `url(${staticFile('img/afraviva-media-logo-3.png')})`,
            backgroundSize: `${LOGO_W}px ${LOGO_H}px`,
            backgroundPosition: `${-c * tw}px ${-r * th}px`,
          }}
        />,
      );
    }
  }
  // Soft glow once everything has landed.
  const glow = interpolate(frame, [50, 62, 90], [0, 0.55, 0.25], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <div style={{position: 'relative', width: LOGO_W, height: LOGO_H, boxShadow: `0 0 80px ${GOLD}`, borderRadius: 6}}>
      <div style={{position: 'absolute', inset: 0, borderRadius: 6, boxShadow: `0 0 120px 20px ${GOLD_LIGHT}`, opacity: glow}} />
      {tiles}
    </div>
  );
};

export const EndCard: React.FC<{contact: string[]; tagline: string; durationInFrames: number}> = ({contact, tagline, durationInFrames}) => {
  const frame = useCurrentFrame();
  const L = useLayout();
  const fadeIn = interpolate(frame, [0, 10], [0, 1], {extrapolateRight: 'clamp'});
  const fadeOut = interpolate(frame, [durationInFrames - 15, durationInFrames], [1, 0], {extrapolateLeft: 'clamp'});
  const textIn = interpolate(frame, [60, 80], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{opacity: fadeIn * fadeOut, background: FOREST, justifyContent: 'center', alignItems: 'center'}}>
      <AssemblingLogo width={L.logoW} />
      <div style={{opacity: textIn, textAlign: 'center'}}>
        <div style={{color: PAPER, fontSize: L.endTitle, fontWeight: 700, marginTop: 36}}>We tell Africa&apos;s story!</div>
        <div style={{color: GOLD_LIGHT, fontSize: L.endTag, marginTop: 4}}>{tagline}</div>
        <div style={{marginTop: 28, color: PAPER, fontSize: L.endContact, lineHeight: 1.5}}>
          {contact.map((c) => (
            <div key={c}>{c}</div>
          ))}
        </div>
      </div>
    </AbsoluteFill>
  );
};

export const Promo: React.FC<PromoProps> = ({title, tagline, scenes, partners, contact, partnersStartSec, endCardStartSec}) => {
  const {fps, durationInFrames} = useVideoConfig();
  const L = useLayout();
  const frame = useCurrentFrame();
  const f = (s: number) => Math.round(s * fps);
  return (
    <AbsoluteFill style={{background: FOREST_DARK, fontFamily}}>
      {/* Original synthesised music (video/tools/make_music.py), ducked under the voice-over. */}
      <Audio
        src={staticFile('audio/promo-bed.mp3')}
        volume={(frame) =>
          interpolate(
            frame,
            [0, f(0.8), f(1.2), f(3.9), f(4.6), f(33), f(33.6), durationInFrames - 45, durationInFrames],
            [0.7, 0.7, 0.4, 0.4, 0.3, 0.3, 0.4, 0.4, 0],
            {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
          )
        }
      />
      {/* AI voice-over (video/tools/make_voice.py, Kokoro), timed to the scene captions. */}
      <Audio src={staticFile('audio/promo-voice.mp3')} volume={1} />

      {/* Source footage is 1280x588, scaled to full width and letterboxed. */}
      <div style={{position: 'absolute', left: 0, top: L.vTop, width: L.width, height: L.vH, overflow: 'hidden'}}>
        {L.vertical ? (
          // Tall crop of the wide footage: scale to window height and pan across it.
          (() => {
            const vw = Math.round((L.vH * 1280) / 588);
            const pan = interpolate(frame, [0, f(42)], [0, -(vw - L.width)], {extrapolateRight: 'clamp'});
            return (
              <OffthreadVideo
                src={staticFile('video/media-hero.mp4')}
                muted
                style={{position: 'absolute', top: 0, left: 0, width: vw, height: L.vH, transform: `translateX(${pan}px)`}}
              />
            );
          })()
        ) : (
          <OffthreadVideo src={staticFile('video/media-hero.mp4')} muted style={{width: '100%', height: '100%', objectFit: 'cover'}} />
        )}
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
