using System;
using System.Collections.Generic;
using System.Linq;
using System.Net;
using System.Net.Http;
using System.Threading.Tasks;
using System.Web.Http;
using ASP.NET_MVC_Application.Extensions;
using ASP.NET_MVC_Application.Models;
using ASP.NET_MVC_Application.Repositories;

namespace ASP.NET_MVC_Application.Controllers
{
    [RoutePrefix("api/v2/products")]
    public class ProductsV2Controller : ApiController
    {
        private readonly ProductRepository _productRepository = new ProductRepository();
        private readonly ProductBlockchainRepository _productBlockchainRepository = new ProductBlockchainRepository();
        private const string Center = "Rob";
        private MachinesRepository _machinesRepository = new MachinesRepository();

        public static bool Aisle1Status { get; set; }
        public static bool Aisle2Status { get; set; }
        public static bool Aisle3Status { get; set; }

        public class AisleStatus
        {
            public int Number { get; set; }
            public bool Status { get; set; }
        }


        // получение продукта по его имени
        [Route("getbyplace"), HttpPost]
        public ProductPickUpModel GetProductByPlace([FromBody] Place place)
        {

            var all = _productRepository.GetAll();
            Product product = all.FirstOrDefault(x => x.Place == place);
            if (product == null)
            {
                ProductPickUpModel EmptyPrdct = new ProductPickUpModel()
                {
                    ProductName = "",
                    Freshness = 2
                };
                return EmptyPrdct;
            }
            ProductPickUpModel prdct = new ProductPickUpModel()
            {
                ProductName = product.Name,
                Freshness = product.ExpirationStatus
            };

            return prdct;
        }

        //Создание нового продукта на перевозку по территории
        [Route("createfromapi"), HttpPost]
        public Product CreateFromApi([FromBody] ProductCreateModel prdct)
        {
            if (prdct == null)
                throw new HttpResponseException(HttpStatusCode.BadRequest);

            var all = _productRepository.GetAll();
            if (prdct.Name == "")
            {
                throw new HttpResponseException(new HttpResponseMessage(HttpStatusCode.BadRequest)
                {
                    Content = new StringContent("Неудачное распознавание")
                });
            }

            var product = new Product
            {
                Name = prdct.Name,
                Supplier = "Поставщик",
                Place = Place.InTransportation1
            };

            product.ExpirationDate = DateTime.Now.AddMonths(1);

            product = _productRepository.Create(product);

            var blockchainComment = $"продукт #{product.Id} {product.Name}:<br/>поступил на склад и находится в {product.Place.GetEnumDescription()} ";

            _productBlockchainRepository.Create(new ProductBlockchain
            {
                Comment = blockchainComment,
                ProductId = product.Id
            });

            return product;
        }

        //Создание нового продукта при наличии всех данных из ЮАЙ(срок, поставщик и тд)
        [Route("create"), HttpPost]
        public Product Create([FromBody] Product product)
        {
            if (product == null)
                throw new HttpResponseException(HttpStatusCode.BadRequest);

            var all = _productRepository.GetAll();
            if (all.Any(x => x.Place == product.Place))
            {
                throw new HttpResponseException(new HttpResponseMessage(HttpStatusCode.BadRequest)
                {
                    Content = new StringContent("Место уже занято")
                });
            }

            product = _productRepository.Create(product);

            var blockchainComment = $"продукт #{product.Id} {product.Name}:<br/>поступил на склад и находится в {product.Place.GetEnumDescription()} ";

            _productBlockchainRepository.Create(new ProductBlockchain
            {
                Comment = blockchainComment,
                ProductId = product.Id
            });

            return product;
        }

        //Обновление продукта
        [Route("update"), HttpPost]
        public Product Update([FromBody] Product product)
        {
            if (product == null)
                throw new HttpResponseException(HttpStatusCode.BadRequest);

            return _productRepository.Update(product);
        }



        //Перевод продукта из перемещения по территории на место на складе
        [Route("moveFromTransportation"), HttpPost]
        public Product MovePlace()
        {
            var all = _productRepository.GetAll();
            if (!all.Any(x => x.Place == Place.InTransportation1))
            {
                throw new HttpResponseException(new HttpResponseMessage(HttpStatusCode.BadRequest)
                {
                    Content = new StringContent("Нет товаров для установки на склад")
                });
            }

            Product product = all.FirstOrDefault(x => x.Place == Place.InTransportation1);

            //var product = _productRepository.GetById(model.ProductId);
            if (product == null)
            {
                throw new HttpResponseException(new HttpResponseMessage(HttpStatusCode.BadRequest)
                {
                    Content = new StringContent("Продукта нет")
                });
            }

            var destArray = GetArray();

            throw new NotImplementedException();

            //var destination = destArray.IndexOf('1');

            //Place destPlace = (Place)destination;

            //var blockchainComment = $"#{product.Id} {product.Name} перемещен из {product.Place.GetEnumDescription()} в {destPlace.GetEnumDescription()}";

            //product.Place = destPlace;
            //_productRepository.Update(product);

            //_productBlockchainRepository.Create(new ProductBlockchain
            //{
            //    Comment = blockchainComment,
            //    ProductId = product.Id
            //});

            //return product;
        }

        //Запись в блокчейн что есть пары этилена
        [Route("checkGaz"), HttpPost]
        public Product checkGaz()
        {
            var all = _productRepository.GetAll();
            if (!all.Any(x => x.Place == Place.InTransportation1))
            {
                throw new HttpResponseException(new HttpResponseMessage(HttpStatusCode.BadRequest)
                {
                    Content = new StringContent("Нет товаров для установки на склад")
                });
            }

            var product = all.FirstOrDefault(x => x.Place == Place.InTransportation1);
            if (product == null)
            {
                throw new HttpResponseException(new HttpResponseMessage(HttpStatusCode.BadRequest)
                {
                    Content = new StringContent("Продукта нет")
                });
            }

            var blockchainComment = $"#{product.Id} {product.Name} содержит повышенные пары этилена";

            product.ExpirationStatus = 4;

            product.Reason = "Этилен";

            _productRepository.Update(product);

            _productBlockchainRepository.Create(new ProductBlockchain
            {
                Comment = blockchainComment,
                ProductId = product.Id,

                TransportationChain = new TransportationChain
                {
                    Freshness = false,
                    Place = Center,
                    Temperature = true
                }
            });

            return product;
        }


        //Запись в блочейн, что паров этилена не обнаружено
        [Route("checkGaznogaz"), HttpPost]
        public Product checkGaznogaz()
        {
            var all = _productRepository.GetAll();
            if (!all.Any(x => x.Place == Place.InTransportation1))
            {
                throw new HttpResponseException(new HttpResponseMessage(HttpStatusCode.BadRequest)
                {
                    Content = new StringContent("Нет товаров для установки на склад")
                });
            }

            Product product = all.FirstOrDefault(x => x.Place == Place.InTransportation1);

            //var product = _productRepository.GetById(model.ProductId);
            if (product == null)
            {
                throw new HttpResponseException(new HttpResponseMessage(HttpStatusCode.BadRequest)
                {
                    Content = new StringContent("Продукта нет")
                });
            }


            var blockchainComment = $"#{product.Id} {product.Name} не содержит паров этилена";

            product.ExpirationStatus = 2;

            _productRepository.Update(product);


            _productBlockchainRepository.Create(new ProductBlockchain
            {
                Comment = blockchainComment,
                ProductId = product.Id,
                TransportationChain = new TransportationChain
                {
                    Freshness = true,
                    Temperature = true,
                    Place = Center
                }
            });

            return product;
        }


        //Смена места продукта на складе
        [Route("move"), HttpPost]
        public Product MovePlace([FromBody] ProductMoveModel model)
        {
            var all = _productRepository.GetAll();
            if (all.Any(x => x.Place == model.Place))
            {
                throw new HttpResponseException(new HttpResponseMessage(HttpStatusCode.BadRequest)
                {
                    Content = new StringContent("Место уже занято")
                });
            }

            var product = _productRepository.GetByName(model.ProductName);
            if (product == null)
            {
                throw new HttpResponseException(new HttpResponseMessage(HttpStatusCode.BadRequest)
                {
                    Content = new StringContent("Продукта нет")
                });
            }

            var blockchainComment = $"#{product.Id} {product.Name} перемещен c {product.Place.GetEnumDescription()} в {model.Place.GetEnumDescription()}";

            product.Place = model.Place;
            if (!model.Freshness)
            {
                product.ExpirationStatus = 4;
            }
            if (model.Freshness)
            {
                product.ExpirationStatus = 2;
            }

            _productRepository.Update(product);

            _productBlockchainRepository.Create(new ProductBlockchain
            {
                Comment = blockchainComment,
                ProductId = product.Id,

                TransportationChain = new TransportationChain
                {
                    Place = Center,
                    Freshness = model.Freshness,
                    Temperature = model.Temperature
                }
            });

            return product;
        }


        //Отправка продукта на распродажу
        [Route("deleteToSales"), HttpPost]
        public void DeleteToSales([FromBody] ProductCreateModel prdct)
        {
            if (prdct.Name == "")
            {
                throw new HttpResponseException(new HttpResponseMessage(HttpStatusCode.BadRequest)
                {
                    Content = new StringContent("Неудачное распознавание")
                });
            }
            Product product = _productRepository.GetByName(prdct.Name);
            if (product == null)
                throw new HttpResponseException(HttpStatusCode.BadRequest);
            var blockchainComment = $"#{product.Id} {product.Name}:<br/>отправлен на быструю реализацию";
            _productRepository.Delete(product);
            _productBlockchainRepository.Create(new ProductBlockchain
            {
                Comment = blockchainComment,
                ProductId = product.Id
            });
        }


        //Отправка продукта на переработку
        [Route("DeleteToRefubrishing"), HttpPost]
        public void DeleteToRefubrishing([FromBody] ProductCreateModel prdct)
        {
            if (prdct.Name == "")
            {
                throw new HttpResponseException(new HttpResponseMessage(HttpStatusCode.BadRequest)
                {
                    Content = new StringContent("Неудачное распознавание")
                });
            }
            Product product = _productRepository.GetByName(prdct.Name);
            if (product == null)
                throw new HttpResponseException(HttpStatusCode.BadRequest);
            var blockchainComment = $"#{product.Id} {product.Name}:<br/>отправлен на переработку";
            _productRepository.Delete(product);
            _productBlockchainRepository.Create(new ProductBlockchain
            {
                Comment = blockchainComment,
                ProductId = product.Id
            });
        }

        [Route("delete"), HttpPost]
        public void Delete([FromBody] Product product)
        {
            if (product == null)
                throw new HttpResponseException(HttpStatusCode.BadRequest);

            _productRepository.Delete(product);
        }


        //Запись в блокчейн о постороннем на территории
        [Route("alert"), HttpPost]
        public void Alert()
        {
            var blockchainComment = $"Обнаружен посторонний на территории";

            _productBlockchainRepository.Create(new ProductBlockchain
            {
                Comment = blockchainComment,
                ProductId = null
            });
        }

        //Получение всех данных из блокчейна для ЮАЙ
        [Route("blockchain"), HttpGet]
        public List<ProductBlockchain> GetHash()
        {
            return _productBlockchainRepository.GetAll();
        }

        //Получение списка всех продуктов
        [Route("list"), HttpGet]
        public List<Product> List()
        {
            return _productRepository.GetAll();
        }

        //Получение продукта по его ID
        [Route("{id:int}"), HttpGet]
        public Product GetById(int id)
        {
            return _productRepository.GetById(id);
        }


        //получение продукта по его имени
        [Route("{name}"), HttpGet]
        public Product GetByName(string name)
        {
            return _productRepository.GetByName(name);
        }


        //Создание массива:
        //Создается массив из всех "1" дальше получаем список продуктов, проходимся по всем полученным продуктам, получаем Айди их мест 
        //и записываем значение их статуса в arrayId=placeId
        [Route("getarray"), HttpGet]
        public List<List<object[]>> GetArray()
        {
            //int[] storagefilling = { 1, 1, 1, 1, 1, 1, 1, 1, 1 };


            var products = _productRepository.GetAll();
            //foreach (Product product in products)
            //{
            //    int i = Convert.ToInt32(product.Place);
            //    if (i == 9) continue;
            //    storagefilling[i] = product.ExpirationStatus;
            //}

            var list = new List<List<object[]>>();


            AddPlaces(list, new[] { Place.Aisle1Place1, Place.Aisle1Place2, Place.Aisle1Place3 }, products);
            AddPlaces(list, new[] { Place.Aisle2Place1, Place.Aisle2Place2, Place.Aisle2Place3 }, products);
            AddPlaces(list, new[] { Place.Aisle3Place1, Place.Aisle3Place2, Place.Aisle3Place3 }, products);


            return list;

            //string result = "";
            //foreach (int i in storagefilling)
            //{
            //    result = result + i.ToString();
            //}

            //return result;
        }

        private void AddPlaces(List<List<object[]>> list, Place[] places, List<Product> products)
        {
            var placeList = new List<object[]>();

            foreach (var item in places)
            {

                var product = products.FirstOrDefault(x => x.Place == item);
                if (product != null)
                {
                    placeList.Add(new object[] { product.Name, product.ExpirationStatus });
                }
                else
                {
                    placeList.Add(new object[] { "", 0 });
                }

            }

            list.Add(placeList);
        }

        //[Route("pickup"), HttpPost]
        //public void ProductPickup([FromBody] ProductPickUpModel prdct)
        //{
        //    if (prdct.ProductName == "")
        //    {
        //        throw new HttpResponseException(new HttpResponseMessage(HttpStatusCode.BadRequest)
        //        {
        //            Content = new StringContent("Неудачное распознавание")
        //        });
        //    }

        //    if (prdct == null)
        //    {
        //        throw new HttpResponseException(new HttpResponseMessage(HttpStatusCode.BadRequest)
        //        {
        //            Content = new StringContent("Продукта нет")
        //        });
        //    }

        //    var destArray = GetArray();

        //    //var destination = destArray.IndexOf('1');

        //    //Place destPlace = (Place)destination;

        //    //Product product = _productRepository.GetByName(prdct.ProductName);
        //    //if (product == null)
        //    //    throw new HttpResponseException(HttpStatusCode.BadRequest);
        //    //var blockchainComment = $"#{product.Id} {product.Name} перемещен из {product.Place.GetEnumDescription()} в {destPlace.GetEnumDescription()}";

        //    //_productBlockchainRepository.Create(new ProductBlockchain
        //    //{
        //    //    Comment = blockchainComment,
        //    //    ProductId = product.Id
        //    //});
        //}

        [Route("updateMachinesStatus"), HttpPost]
        public void UpdateMachineStatus([FromBody]Machines model)
        {
            var machines = _machinesRepository.GetAll();
            foreach (var item in machines)
            {
                _machinesRepository.Delete(item);
            }

            _machinesRepository.Create(model);
        }

        [Route("getMachinesStatus"), HttpGet]
        public Machines GetMachinesStatus()
        {
            var machines = _machinesRepository.GetAll().FirstOrDefault();

            if (machines == null)
            {
                return new Machines
                {
                    MachineIncome = MachineStatus.No,
                    MachineOutcome = MachineStatus.No,
                    MachineUtilization = MachineStatus.No
                };
            }

            return machines;
        }

        [Route("addChain"), HttpPost]
        public IHttpActionResult AddChain(ProductBlockchainModel model)
        {
            var product = _productRepository.GetByName(model.ProductName);
            if(product == null)
            {
                return BadRequest("Нет такого продукта");
            }

            _productBlockchainRepository.Create(new ProductBlockchain
            {
                Comment = model.Comment,
                ProductId = product.Id,
                TransportationChain = model.TransportationChain
            });

            return Ok();
        }

        [Route("verifyAisleIsBusy/{aisle:int}"), HttpGet]
        public bool VerifyAisleIsBusy(int aisle)
        {
            if (aisle == 0) return Aisle1Status;
            if (aisle == 1) return Aisle2Status;
            if (aisle == 2) return Aisle3Status;
            else
                return true;
        }

        [Route("IsBusy"), HttpPost]
        public void IsBusy([FromBody] AisleStatus aisleStatus)
        {
            if (aisleStatus.Number == 0) Aisle1Status = aisleStatus.Status;
            if (aisleStatus.Number == 1) Aisle2Status = aisleStatus.Status;
            if (aisleStatus.Number == 2) Aisle3Status = aisleStatus.Status;
        }

    }

    
}