export class InvalidUiElementError extends Error {
  constructor(operation: string, currentTarget: EventTarget | null) {
    const targetInfo = currentTarget ? `Type: ${currentTarget.constructor?.name}` : 'null'
    super(
      `Operation "${operation}" failed: e.currentTarget is not an HTMLElement. Actual target: ${targetInfo}.`,
    )
    this.name = 'InvalidUiElementError'
  }
}
