export declare class Observation {
    readonly kore: number[];
    readonly playerHlt: number[];
    readonly playerShipyards: Map<string, number[]>[];
    readonly playerFleets: Map<string, string[]>[];
    readonly player: number;
    readonly step: number;
    readonly remainingOverageTime: number;
    constructor(rawObservation: string);
}
