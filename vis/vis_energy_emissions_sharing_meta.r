###VISUALISE MODEL OUTPUTS###
library(tidyverse)
library(ggpubr)

my_list = list(
  c("COL", "Colombia")#,
)


for(i in 1:length(my_list)) {

print(i)
iso3 = my_list[[i]][1]
country_name = my_list[[i]][2]

# iso3 = 'COL'
# country_name = 'Colombia'
# print(iso3)
  
folder <- dirname(rstudioapi::getSourceEditorContext()$path)

filename = 'emissions_national_generate_shared_power_options.csv'
data <- read.csv(file.path(folder, '..', 'results', 'model_results', iso3, filename))
names(data)[names(data) == 'GID_0'] <- 'country'

data$scenario_adopt = ''
data$scenario_adopt[grep("high", data$scenario)] = 'high'
data$scenario_adopt[grep("baseline", data$scenario)] = 'baseline'
data$scenario_adopt[grep("low", data$scenario)] = 'low'

data$scenario_capacity = ''
data$scenario_capacity[grep("50_50_50", data$scenario)] = '50 GB Per Month'

data$scenario_sharing = ''
data$scenario_sharing[grep("baseline_baseline_baseline_baseline_baseline", data$strategy)] = 'Baseline'
data$scenario_sharing[grep("passive_baseline_baseline_baseline_baseline", data$strategy)] = 'Passive'
data$scenario_sharing[grep("active_baseline_baseline_baseline_baseline", data$strategy)] = 'Active'
data$scenario_sharing[grep("srn_baseline_baseline_baseline_baseline", data$strategy)] = 'SRN'

data$strategy_short = ''
# data$strategy_short[grep("3G_umts_fiber", data$strategy)] = '3G (F)'
# data$strategy_short[grep("3G_umts_wireless", data$strategy)] = '3G (W)'
data$strategy_short[grep("4G_epc_fiber", data$strategy)] = '4G (F)'
data$strategy_short[grep("4G_epc_wireless", data$strategy)] = '4G (W)'
data$strategy_short[grep("5G_nsa_fiber", data$strategy)] = '5G (F)'
data$strategy_short[grep("5G_nsa_wireless", data$strategy)] = '5G (W)'

data$strategy_short = factor(data$strategy_short, levels=c(
                                     # "3G (F)",
                                     "4G (F)",
                                     '5G (F)',
                                     # "3G (W)",
                                     "4G (W)",
                                     '5G (W)'
                                     ))

data$scenario_sharing = factor(data$scenario_sharing,
                                levels=c("Baseline",
                                         "Passive",
                                         "Active", 
                                         'SRN'
                                         ))

data = data[complete.cases(data),]

data <- select(data,
               scenario_adopt, scenario_sharing, strategy_short, #grid_type,
               total_energy_annual_demand_kwh,
               total_demand_carbon_per_kwh,
               total_nitrogen_oxide_per_kwh,
               total_sulpher_dioxide_per_kwh,
               total_pm10_per_kwh)

data = data %>%
  group_by(scenario_adopt, scenario_sharing, strategy_short) %>%
  summarise(
    total_energy_annual_demand_kwh = sum(total_energy_annual_demand_kwh),
    total_demand_carbon_per_kwh = sum(total_demand_carbon_per_kwh),
    total_nitrogen_oxide_per_kwh = sum(total_nitrogen_oxide_per_kwh),
    total_sulpher_dioxide_per_kwh = sum(total_sulpher_dioxide_per_kwh),
    total_pm10_per_kwh = sum(total_pm10_per_kwh)
    )

############
sample <- data %>%
  group_by(scenario_adopt, scenario_sharing, strategy_short) %>% #, grid_type
  summarize(
    value = round(sum(total_energy_annual_demand_kwh)),
  )

sample$value = sample$value / 1e9

min_value = min(round(sample$value))
max_value = max(round(sample$value)) + 1
min_value[min_value > 0] = 0

sample = spread(sample, scenario_adopt, value)

totals <- sample %>%
  group_by(scenario_sharing, strategy_short) %>%
  summarize(value2 = round(
    (baseline), 1))

energy =
  ggplot(sample,
  aes(x=strategy_short, y=baseline, fill=strategy_short)) +
  geom_bar(stat="identity", position=position_dodge()) +
  geom_errorbar(data=sample, aes(y = baseline, ymin = low, ymax = high),
                position = position_dodge(width = .9), lwd = 0.5,
                show.legend = FALSE, width=0.1,  color="#FF0000FF") +
  geom_text(y=0, aes(strategy_short, value2, label = value2, color="#FF0000FF"),
            size = 3, data = totals, vjust=-.5, hjust=.5) +
  theme(legend.position = 'none',
        axis.text.x = element_text(angle = 45, hjust=1)) +
  labs(title = "Total Universal Broadband Energy Demand 2020-2030 by Infrastructure Sharing Strategy",
       fill=NULL,
       subtitle = paste("Interval bars reflect estimates for low and high adoption scenarios for", country_name),
       x = NULL, y = "Terawatt hours (TWh)") +
  scale_y_continuous(expand = c(0, 0), limits = c(0, max_value)) +
  scale_fill_viridis_d() +
  facet_grid(~scenario_sharing)

############
sample <- data %>%
  group_by(scenario_adopt, scenario_sharing, strategy_short) %>% #, grid_type
  summarize(
    value = round(sum(total_demand_carbon_per_kwh)),
  )

sample$value = sample$value / 1e6

min_value = min(round(sample$value))
max_value = max(round(sample$value)) + 1
min_value[min_value > 0] = 0

sample = spread(sample, scenario_adopt, value)

totals <- sample %>%
  group_by(scenario_sharing, strategy_short) %>%
  summarize(value2 = round(
    (baseline), 0))

carbon_dioxide = ggplot(sample,
                aes(x=strategy_short, y=baseline, fill=strategy_short)) +
  geom_bar(stat="identity", position=position_dodge()) +
  geom_errorbar(data=sample, aes(y = baseline, ymin = low, ymax = high),
                position = position_dodge(width = .9), lwd = 0.5,
                show.legend = FALSE, width=0.1,  color="#FF0000FF") +
  geom_text(y=0, aes(strategy_short, value2, label = value2, color="#FF0000FF"),
            size = 3, data = totals, vjust=-.5, hjust=.5) +
  theme(legend.position = 'none',
        axis.text.x = element_text(angle = 45, hjust=1)) +
       labs(title=expression(paste("Universal Broadband Emissions 2020-2030 (", CO[2], ") by Infrastructure Sharing Strategy")),
       fill=NULL,
       subtitle = paste("Interval bars reflect estimates for low and high adoption scenarios for", country_name),
       x=NULL, y=expression(paste("Kilotonnes of ", CO[2])),sep="") +
  scale_y_continuous(expand = c(0, 0), limits = c(0, max_value)) +
  scale_fill_viridis_d() +
  facet_grid(~scenario_sharing)

dir.create(file.path(folder, 'figures', iso3), showWarnings = FALSE)
path = file.path(folder, 'figures', iso3, 'carbon_sharing.png')
ggsave(path, units="in", width=8, height=4, dpi=300)
dir.create(file.path(folder, '..', 'reports', 'images', iso3), showWarnings = FALSE)
path = file.path(folder, '..', 'reports', 'images', iso3, 'carbon_sharing.png')
ggsave(path, units="in", width=8, height=4, dpi=300)
while (!is.null(dev.list()))  dev.off()

############
sample <- data %>%
  group_by(scenario_adopt, scenario_sharing, strategy_short) %>% #, grid_type
  summarize(
    value = round(sum(total_nitrogen_oxide_per_kwh)),
  )

sample$value = sample$value / 1e3

min_value = min(round(sample$value))
max_value = max(round(sample$value)) + 1
min_value[min_value > 0] = 0

sample = spread(sample, scenario_adopt, value)

totals <- sample %>%
  group_by(scenario_sharing, strategy_short) %>%
  summarize(value2 = round(baseline, 0))

nitrogen_dioxide = ggplot(sample,
                        aes(x=strategy_short, y=baseline, fill=strategy_short)) +
  geom_bar(stat="identity", position=position_dodge()) +
  geom_errorbar(data=sample, aes(y = baseline, ymin = low, ymax = high),
                position = position_dodge(width = .9), lwd = 0.5,
                show.legend = FALSE, width=0.1,  color="#FF0000FF") +
  geom_text(y=0, aes(strategy_short, value2, label = value2, color="#FF0000FF"),
            size = 3, data = totals, vjust=-.5, hjust=.5) +
  theme(legend.position = 'none',
        axis.text.x = element_text(angle = 45, hjust=1)) +
  labs(title=expression(paste("Universal Broadband Emissions 2020-2030 (", NO[x], ") by Infrastructure Sharing Strategy")),
    # title = "Universal Broadband Emissions for Colombia 2020-2030 (Nitrogen Oxides)",
       fill=NULL,
       subtitle = paste("Interval bars reflect estimates for low and high adoption scenarios for", country_name),
       x = NULL, y=expression(paste("Tonnes of ", NO[x])), sep="")  +
  scale_y_continuous(expand = c(0, 0), limits = c(0, max_value)) +
  scale_fill_viridis_d() +
  facet_grid(~scenario_sharing)

############
sample <- data %>%
  group_by(scenario_adopt, scenario_sharing, strategy_short) %>% #, grid_type
  summarize(
    value = round(sum(total_sulpher_dioxide_per_kwh)),
  )

sample$value = sample$value / 1e6

min_value = min(round(sample$value))
max_value = max(round(sample$value)) + 1
min_value[min_value > 0] = 0

sample = spread(sample, scenario_adopt, value)

totals <- sample %>%
  group_by(scenario_sharing, strategy_short) %>%
  summarize(value2 = round(baseline, 1))

suplher_dioxide = ggplot(sample,
                          aes(x=strategy_short, y=baseline, fill=strategy_short)) +
  geom_bar(stat="identity", position=position_dodge()) +
  geom_errorbar(data=sample, aes(y = baseline, ymin = low, ymax = high),
                position = position_dodge(width = .9), lwd = 0.5,
                show.legend = FALSE, width=0.1,  color="#FF0000FF") +
  geom_text(y=0, aes(strategy_short, value2, label = value2, color="#FF0000FF"),
            size = 3, data = totals, vjust=-.5, hjust=.5) +
  theme(legend.position = 'none',
        axis.text.x = element_text(angle = 45, hjust=1)) +
  labs(title=expression(paste("Universal Broadband Emissions 2020-2030 (", SO[x], ") by Infrastructure Sharing Strategy")),
    # title = "Universal Broadband Emissions for Colombia 2020-2030 (Sulphur Oxides)",
       fill=NULL,
       subtitle = paste("Interval bars reflect estimates for low and high adoption scenarios for", country_name),
       x = NULL, y=expression(paste("Tonnes of ", SO[x])), sep="") +
  scale_y_continuous(expand = c(0, 0), limits = c(0, max_value)) +
  scale_fill_viridis_d() +
  facet_grid(~scenario_sharing)

############

sample <- data %>%
  group_by(scenario_adopt, scenario_sharing, strategy_short) %>% #, grid_type
  summarize(
    value = round(sum(total_pm10_per_kwh)),
  )

sample$value = sample$value / 1e6

min_value = min(round(sample$value))
max_value = max(round(sample$value)) + 1
min_value[min_value > 0] = 0

sample = spread(sample, scenario_adopt, value)

totals <- sample %>%
  group_by(scenario_sharing, strategy_short) %>%
  summarize(value2 = round(baseline, 1))

pm10 = ggplot(sample,
                         aes(x=strategy_short, y=baseline, fill=strategy_short)) +
  geom_bar(stat="identity", position=position_dodge()) +
  geom_errorbar(data=sample, aes(y = baseline, ymin = low, ymax = high),
                position = position_dodge(width = .9), lwd = 0.5,
                show.legend = FALSE, width=0.1,  color="#FF0000FF") +
  geom_text(y=0, aes(strategy_short, value2, label = value2, color="#FF0000FF"),
            size = 3, data = totals, vjust=-.5, hjust=.5) +
  theme(legend.position = 'none',
        axis.text.x = element_text(angle = 45, hjust=1)) +
  labs(title=expression(paste("Universal Broadband Emissions 2020-2030 (", PM[10], ") by Infrastructure Sharing Strategy")),
       fill=NULL,
       subtitle = paste("Interval bars reflect estimates for low and high adoption scenarios for", country_name),
       x = NULL, y=expression(paste("Kilotonnes of ", PM[10])), sep="") + #y ="Tonnes of PM10") +
  scale_y_continuous(expand = c(0, 0), limits = c(0, max_value)) +
  scale_fill_viridis_d() +
  facet_grid(~scenario_sharing)

############
ggarrange(
  energy,
  carbon_dioxide,
  labels = c("A", "B"),
  ncol = 1, nrow = 2)

dir.create(file.path(folder, 'figures', iso3), showWarnings = FALSE)
path = file.path(folder, 'figures', iso3, 'energy_emissions_sharing.png')
ggsave(path, units="in", width=8, height=7, dpi=300)
dir.create(file.path(folder, '..', 'reports', 'images', iso3), showWarnings = FALSE)
path = file.path(folder, '..', 'reports', 'images', iso3, 'energy_emissions_sharing.png')
ggsave(path, units="in", width=8, height=7, dpi=300)
while (!is.null(dev.list()))  dev.off()

ggarrange(
  nitrogen_dioxide,
  suplher_dioxide,
  pm10,
  labels = c("A", "B", "C"),
  ncol = 1, nrow = 3)

dir.create(file.path(folder, 'figures', iso3), showWarnings = FALSE)
path = file.path(folder, 'figures', iso3, 'health_emissions_sharing.png')
ggsave(path, units="in", width=8, height=10, dpi=300)
dir.create(file.path(folder, '..', 'reports', 'images', iso3), showWarnings = FALSE)
path = file.path(folder, '..', 'reports', 'images', iso3, 'health_emissions_sharing.png')
ggsave(path, units="in", width=8, height=10, dpi=300)
while (!is.null(dev.list()))  dev.off()

}
