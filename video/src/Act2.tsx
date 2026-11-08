import {AbsoluteFill, Audio, OffthreadVideo, Sequence, interpolate, staticFile, useCurrentFrame, useVideoConfig} from 'remotion';
import {z} from 'zod';
import {loadFont} from '@remotion/google-fonts/Poppins';
import timeline from './act2-timeline.json';

const {fontFamily} = loadFont('normal', {weights: ['400', '600', '700'], subsets: ['latin']});

const GOLD = '#B98A46';
const GOLD_LIGHT = '#CDAB7A';
const PAPER = '#FBF9F2';

type Mode = 'warm' | 'serious' | 'rising' | 'majestic';

export const act2Schema = z.object({
  // Optional footage under the text, e.g. {src: 'video/clips/act2-1.mp4', startSec: 3, endSec: 30}.
  // Files live in static/ (gitignored under static/video/clips/ if third-party).
  footage: z.array(z.object({src: z.string(), startSec: z.number(), endSec: z.number()})),
  footageOpacity: z.number(),
});
export type Act2Props = z.infer<typeof act2Schema>;
export const act2DefaultProps: Act2Props = {footage: [], footageOpacity: 0.45};
export const ACT2_FPS = 30;
export const act2Duration = () => Math.round(timeline.durationSec * ACT2_FPS);

const BACKGROUNDS: Record<Mode, string> = {
  warm: 'radial-gradient(ellipse at 50% 40%, #6b4a2e 0%, #3E2A1B 55%, #231810 100%)',
  serious: 'radial-gradient(ellipse at 50% 60%, #26302b 0%, #141a17 60%, #0a0d0b 100%)',
  rising: 'radial-gradient(ellipse at 50% 40%, #3f6a52 0%, #2C4A3B 55%, #1B2F26 100%)',
  majestic: 'radial-gradient(ellipse at 50% 35%, #d9b26a 0%, #8A6323 35%, #2C4A3B 75%, #14231c 100%)',
};

const sections = timeline.sections as {mode: Mode; startSec: number}[];

const Background: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  return (
    <AbsoluteFill>
      {sections.map((s, i) => {
        const next = sections[i + 1];
        const fadeIn = i === 0 ? 1 : interpolate(t, [s.startSec - 1.5, s.startSec + 0.5], [0, 1], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
        const fadeOut = next ? interpolate(t, [next.startSec - 1.5, next.startSec + 0.5], [1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'}) : 1;
        return <AbsoluteFill key={s.mode} style={{background: BACKGROUNDS[s.mode], opacity: Math.min(fadeIn, fadeOut)}} />;
      })}
    </AbsoluteFill>
  );
};

// Slowly turning light rays that appear with the choir.
const Rays: React.FC = () => {
  const frame = useCurrentFrame();
  const {fps} = useVideoConfig();
  const t = frame / fps;
  const maj = sections.find((s) => s.mode === 'majestic')!.startSec;
  const opacity = interpolate(t, [maj - 0.5, maj + 4], [0, 0.35], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{opacity, mixBlendMode: 'screen'}}>
      <AbsoluteFill
        style={{
          background: `repeating-conic-gradient(from ${frame * 0.12}deg at 50% 38%, rgba(255,230,160,0.55) 0deg 4deg, transparent 4deg 14deg)`,
          maskImage: 'radial-gradient(circle at 50% 38%, black 0%, transparent 70%)',
          WebkitMaskImage: 'radial-gradient(circle at 50% 38%, black 0%, transparent 70%)',
        }}
      />
    </AbsoluteFill>
  );
};

const Line: React.FC<{text: string; mode: Mode; durationInFrames: number}> = ({text, mode, durationInFrames}) => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 10, durationInFrames - 10, durationInFrames], [0, 1, 1, 0], {
    extrapolateLeft: 'clamp',
    extrapolateRight: 'clamp',
  });
  const rise = interpolate(frame, [0, 16], [mode === 'serious' ? 8 : 24, 0], {extrapolateRight: 'clamp'});
  const size = text.length <= 40 ? 104 : text.length <= 90 ? 80 : 62;
  const words = text.split(' ');
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', padding: '0 190px'}}>
      <div style={{opacity, transform: `translateY(${rise}px)`, textAlign: 'center', fontSize: size, lineHeight: 1.25, fontWeight: 600, color: PAPER, textShadow: '0 4px 30px rgba(0,0,0,0.7)'}}>
        {words.map((w, i) => {
          const yes = /^YES/.test(w);
          return (
            <span key={i} style={yes ? {color: GOLD_LIGHT, fontWeight: 700, fontSize: size * 1.15} : undefined}>
              {w}
              {i < words.length - 1 ? ' ' : ''}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const TitleCard: React.FC = () => {
  const frame = useCurrentFrame();
  const opacity = interpolate(frame, [0, 15, 55, 75], [0, 1, 1, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return (
    <AbsoluteFill style={{justifyContent: 'center', alignItems: 'center', opacity, textAlign: 'center'}}>
      <div style={{color: GOLD_LIGHT, fontSize: 44, letterSpacing: 12, fontWeight: 600}}>ACT II</div>
      <div style={{color: PAPER, fontSize: 96, fontWeight: 700, marginTop: 16}}>The Family That Says Yes</div>
    </AbsoluteFill>
  );
};

export const Act2: React.FC<Act2Props> = ({footage, footageOpacity}) => {
  const {fps, durationInFrames} = useVideoConfig();
  const f = (s: number) => Math.round(s * fps);
  const lines = timeline.lines as {text: string; mode: Mode; startSec: number; endSec: number}[];
  const voiceEnd = timeline.voiceEndSec;
  const secT = (mode: Mode) => sections.find((s) => s.mode === mode)!.startSec;
  return (
    <AbsoluteFill style={{background: '#000', fontFamily}}>
      <Background />
      {footage.map((c) => (
        <Sequence key={c.src + c.startSec} from={f(c.startSec)} durationInFrames={f(c.endSec - c.startSec)}>
          <FootageLayer src={c.src} opacity={footageOpacity} durationInFrames={f(c.endSec - c.startSec)} />
        </Sequence>
      ))}
      <Rays />
      <AbsoluteFill style={{background: 'radial-gradient(ellipse at center, transparent 45%, rgba(0,0,0,0.55) 100%)'}} />

      <Sequence from={0} durationInFrames={f(2.5)}>
        <TitleCard />
      </Sequence>
      {lines.map((l) => (
        <Sequence key={l.startSec} from={f(l.startSec)} durationInFrames={f(l.endSec - l.startSec) + 8}>
          <Line text={l.text} mode={l.mode} durationInFrames={f(l.endSec - l.startSec) + 8} />
        </Sequence>
      ))}

      {/* Music (video/tools/make_act2_music.py) dips under the voice and swells at the end. */}
      <Audio
        src={staticFile('audio/act2-music.mp3')}
        volume={(frame) =>
          interpolate(
            frame,
            [0, f(1.8), f(2.8), f(secT('serious')), f(secT('serious') + 2), f(secT('rising')), f(secT('majestic')), f(voiceEnd - 0.5), f(voiceEnd + 2), durationInFrames],
            [0.8, 0.8, 0.5, 0.5, 0.42, 0.5, 0.62, 0.62, 0.9, 0.9],
            {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'},
          )
        }
      />
      {/* Narration (video/tools/make_narration.py, Kokoro AI voice). */}
      <Audio src={staticFile('audio/act2-voice.mp3')} volume={1} />
    </AbsoluteFill>
  );
};

const FootageLayer: React.FC<{src: string; opacity: number; durationInFrames: number}> = ({src, opacity, durationInFrames}) => {
  const frame = useCurrentFrame();
  const o = interpolate(frame, [0, 20, durationInFrames - 20, durationInFrames], [0, opacity, opacity, 0], {extrapolateLeft: 'clamp', extrapolateRight: 'clamp'});
  return <OffthreadVideo src={staticFile(src)} muted style={{width: '100%', height: '100%', objectFit: 'cover', opacity: o}} />;
};
