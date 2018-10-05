using System.Collections.Generic;

namespace ASP.NET_MVC_Application.Models
{
    public class ProductCreateModel
    {
        public string Name { get; set; }
    }

    public class PlacesModel
    {
        public int ChangeInitiatorRobotId { get; set; }

        public Dictionary<Place, ProductModel> Places { get; set; }
    }

}