# Nautobot EVPN


This represents a Nautobot plugin for EVPN management. This creates some resources to fully document a EVPN-based setup in Nautobot.

## Integration 

To integrate this plugin, please add `nautobot-change` to PLUGINS in your Nautobot settings.

### Migration from `nautobot-change`

We seperated `nautobot-change` and `nautobot-evpn` at some point in time. Data is not migrated automagically due to Django restrictions.
This means some manual steps to migrate the data.

1. Migrate `nautobot-change` to the latest point. We just ignore the EVPN tables at some point.
2. Migrate `nautbot-vpn` to 0001. This creates the basic tables.
3. Move `nautbot_change_{anycastdummyip,anycastip,ethernetsegment,ethernetsegmentmembership,vlanvrf,vlanvrflist}` to `nautobot_evpn_{anycastdummyip,anycastip,ethernetsegment,ethernetsegmentmembership,vlanvrf,vlanvrflist}`
4. Do a full migration.
5. Have Fun!