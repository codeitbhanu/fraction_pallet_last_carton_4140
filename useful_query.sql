SELECT stb_num, pe.pcb_num, dsd.cdsn_iuc
FROM stb_production.dbo.production_event pe
    INNER JOIN stb_production.dbo.device_state_dsd_4140 dsd ON dsd.id_production_event = pe.id_production_event
WHERE carton_num = 'CC0000066404' --Enter the last carton having partial units