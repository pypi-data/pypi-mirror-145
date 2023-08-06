from torch import nn

__all__ = ['MLP']


class MLP(nn.Module):
    def __init__(self, input_dim, hidden_dim=None, output_dim=None, num_layers=2, drop=0., act_layer=nn.GELU):
        super().__init__()
        self.net = nn.ModuleList()
        output_dim = output_dim or input_dim
        hidden_dim = hidden_dim or input_dim
        if num_layers == 1:
            self.net.append(nn.Sequential(nn.Linear(input_dim, output_dim), nn.Dropout(drop)))
        else:
            self.net.append(nn.Sequential(nn.Linear(input_dim, hidden_dim), act_layer(), nn.Dropout(drop)))
            for _ in range(num_layers - 2):
                self.net.append(nn.Sequential(nn.Linear(hidden_dim, hidden_dim), act_layer(), nn.Dropout(drop)))
            self.net.append(nn.Sequential(nn.Linear(hidden_dim, output_dim), nn.Dropout(drop)))
        self.net = nn.Sequential(*self.net)

    def forward(self, x):
        return self.net(x)
