import {AddStringIfExists} from "../../utils/addStringIfExists";
import {ReactNode} from "react";


type TextProps = {
    ExtraClasses?: string
    children: ReactNode | ReactNode[];
}

export const ReactMassiveTitleContainer = (props: TextProps) => {
    return (
        <div
            className={"text-2xl sm:text-3xl !leading-snug lg:text-[48px] " + " " + AddStringIfExists(props.ExtraClasses)}>
            {props.children}
        </div>
    )
}

export const ReactSecondaryTitleContainer = (props: TextProps) => {
    return (
        <div className={"text-2xl lg:text-3xl leading-normal" + " " + AddStringIfExists(props.ExtraClasses)}>
            {props.children}
        </div>
    )
}

export const ReactTertiaryTitleContainer = (props: TextProps) => {
    return (
        <div className={"text-[24px] lg:text-[28px] leading-normal" + " " +AddStringIfExists(props.ExtraClasses)}>
            {props.children}
        </div>
    )
}

export const ReactBigTextContainer = (props: TextProps) => {
    return (
        <div className={"sm:text-xl leading-normal " + " " +AddStringIfExists(props.ExtraClasses)}>
            {props.children}
        </div>
    )
}

export const ReactMediumTextContainer = (props: TextProps) => {
    return (
        <div className={"text-[19px] sm:text-[21px] leading-normal " + " " + AddStringIfExists(props.ExtraClasses)}>
            {props.children}
        </div>
    )
}

export const ReactNormalTextContainer = (props: TextProps) => {
    return (
        <div className={"text-[19px] leading-normal " + " " + AddStringIfExists(props.ExtraClasses)}>
            {props.children}
        </div>
    )
}