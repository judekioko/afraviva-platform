import {Composition} from 'remotion';
import {Intro, introSchema} from './Intro';
import {ACT2_FPS, Act2, act2DefaultProps, act2Duration, act2Schema} from './Act2';
import {CLIP_FPS, ClipBranded, clipBrandedDefaultProps, clipBrandedDuration, clipBrandedSchema} from './ClipBranded';
import {PROMO_DURATION_SEC, PROMO_FPS, Promo, promoDefaultProps, promoSchema} from './Promo';

export const RemotionRoot: React.FC = () => {
  return (
    <>
    <Composition
      id="Promo"
      component={Promo}
      schema={promoSchema}
      durationInFrames={PROMO_DURATION_SEC * PROMO_FPS}
      fps={PROMO_FPS}
      width={1920}
      height={1080}
      defaultProps={promoDefaultProps}
    />
    <Composition
      id="Act2"
      component={Act2}
      schema={act2Schema}
      durationInFrames={act2Duration()}
      fps={ACT2_FPS}
      width={1920}
      height={1080}
      defaultProps={act2DefaultProps}
    />
    <Composition
      id="ClipBranded"
      component={ClipBranded}
      schema={clipBrandedSchema}
      durationInFrames={clipBrandedDuration(clipBrandedDefaultProps)}
      fps={CLIP_FPS}
      width={1080}
      height={1920}
      defaultProps={clipBrandedDefaultProps}
      calculateMetadata={({props}) => ({durationInFrames: clipBrandedDuration(props)})}
    />
    <Composition
      id="PromoVertical"
      component={Promo}
      schema={promoSchema}
      durationInFrames={PROMO_DURATION_SEC * PROMO_FPS}
      fps={PROMO_FPS}
      width={1080}
      height={1920}
      defaultProps={promoDefaultProps}
    />
    <Composition
      id="Intro"
      component={Intro}
      schema={introSchema}
      durationInFrames={150}
      fps={30}
      width={1920}
      height={1080}
      defaultProps={{
        title: 'AfraViva',
        subtitle: 'Stories from the heart of Africa',
      }}
    />
    </>
  );
};
