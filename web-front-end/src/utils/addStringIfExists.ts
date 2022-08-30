export const AddStringIfExists = (s: string | undefined): string => {
    if (s) {
        return " " + s
    }
    return ""
}